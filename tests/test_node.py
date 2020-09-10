"""Define tests for the "Node" object."""
import tempfile
from unittest.mock import MagicMock, PropertyMock, mock_open

import aiohttp
import pytest
import smb

from pyairvisual import CloudAPI
from pyairvisual.errors import NodeProError
from pyairvisual.node import NodeSamba

from tests.async_mock import patch
from tests.common import (
    TEST_API_KEY,
    TEST_NODE_ID,
    TEST_NODE_IP_ADDRESS,
    TEST_NODE_PASSWORD,
    load_fixture,
)


@pytest.mark.asyncio
async def test_node_by_id(aresponses):
    """Test getting a node's info by its ID from the cloud API."""
    aresponses.add(
        "www.airvisual.com",
        "/api/v2/node/12345",
        "get",
        aresponses.Response(
            text=load_fixture("node_by_id_response.json"),
            headers={"Content-Type": "application/json"},
            status=200,
        ),
    )

    async with aiohttp.ClientSession() as session:
        cloud_api = CloudAPI(TEST_API_KEY, session=session)
        data = await cloud_api.node.get_by_node_id(TEST_NODE_ID)
        assert data["current"]["tp"] == 2.3
        assert data["current"]["hm"] == 73
        assert data["current"]["p2"] == 35
        assert data["current"]["co"] == 479


@pytest.mark.asyncio
async def test_node_by_samba():
    """Test getting a node's info over the local network (via Samba)."""
    # Mock the tempfile that current measurements get loaded into:
    measurements_response = load_fixture("node_measurements_samba_response.json")
    mock_measurements_tmp_file = MagicMock()
    mock_measurements_tmp_file.read.return_value = measurements_response.encode()

    # Mock the history file that SMBConnection returns:
    mock_history_tmp_file = MagicMock()
    type(mock_history_tmp_file).name = PropertyMock(
        return_value="202003_AirVisual_values.txt"
    )

    # Mock the tempfile that history data gets loaded into:
    mock_history_file = MagicMock()
    type(mock_history_file).filename = PropertyMock(
        return_value="202003_AirVisual_values.txt"
    )

    # Mock opening the history file into a CSV reader:
    mop = mock_open(read_data=load_fixture("node_history_samba_response.txt"))
    mop.return_value.__iter__ = lambda self: self
    mop.return_value.__next__ = lambda self: next(iter(self.readline, ""))

    with patch.object(
        tempfile,
        "NamedTemporaryFile",
        side_effect=[mock_measurements_tmp_file, mock_history_tmp_file],
    ), patch("smb.SMBConnection.SMBConnection.connect"), patch(
        "smb.SMBConnection.SMBConnection.listPath", return_value=[mock_history_file]
    ), patch(
        "smb.SMBConnection.SMBConnection.retrieveFile",
    ), patch(
        "smb.SMBConnection.SMBConnection.close"
    ), patch(
        "builtins.open", mop
    ):
        async with NodeSamba(TEST_NODE_IP_ADDRESS, TEST_NODE_PASSWORD) as node:
            measurements = await node.async_get_latest_measurements()
            history = await node.async_get_history()

        assert measurements["measurements"]["co2"] == "442"
        assert measurements["measurements"]["humidity"] == "35"
        assert measurements["measurements"]["pm0_1"] == "3"
        assert measurements["measurements"]["pm1_0"] == "4"
        assert measurements["measurements"]["aqi_cn"] == "6"
        assert measurements["measurements"]["aqi_us"] == "17"
        assert measurements["measurements"]["pm2_5"] == "4.0"
        assert measurements["measurements"]["temperature_C"] == "19.3"
        assert measurements["measurements"]["temperature_F"] == "66.8"
        assert measurements["measurements"]["voc"] == "-1"

        assert len(history["measurements"]) == 7

        assert history["trends"] == {
            "aqi_cn": "decreasing",
            "aqi_us": "decreasing",
            "co2": "decreasing",
            "humidity": "increasing",
            "pm0_1": "decreasing",
            "pm1_0": "decreasing",
            "pm2_5": "decreasing",
            "voc": "flat",
        }


@pytest.mark.asyncio
async def test_node_by_samba_connect_errors():
    """Test various errors arising during connection."""
    node = NodeSamba(TEST_NODE_IP_ADDRESS, TEST_NODE_PASSWORD)

    with patch(
        "smb.SMBConnection.SMBConnection.connect", side_effect=smb.base.NotReadyError,
    ):
        with pytest.raises(NodeProError) as err:
            await node.async_connect()
        assert "The Node/Pro unit can't be connected to: " in str(err)

    with patch(
        "smb.SMBConnection.SMBConnection.connect", side_effect=smb.base.SMBTimeout,
    ):
        with pytest.raises(NodeProError) as err:
            await node.async_connect()
        assert "Timed out while connecting to the Node/Pro unit" in str(err)

    with patch(
        "smb.SMBConnection.SMBConnection.connect", side_effect=ConnectionRefusedError,
    ):
        with pytest.raises(NodeProError) as err:
            await node.async_connect()
        assert "Couldn't find a Node/Pro unit at IP address: 192.168.1.100" in str(err)


@pytest.mark.asyncio
async def test_node_by_samba_fewer_trend_measurements():
    """Test getting a node's trends with a configured number of measurements."""
    # Mock the tempfile that current measurements get loaded into:
    measurements_response = load_fixture("node_measurements_samba_response.json")
    mock_measurements_tmp_file = MagicMock()
    mock_measurements_tmp_file.read.return_value = measurements_response.encode()

    # Mock the history file that SMBConnection returns:
    mock_history_tmp_file = MagicMock()
    type(mock_history_tmp_file).name = PropertyMock(
        return_value="202003_AirVisual_values.txt"
    )

    # Mock the tempfile that history data gets loaded into:
    mock_history_file = MagicMock()
    type(mock_history_file).filename = PropertyMock(
        return_value="202003_AirVisual_values.txt"
    )

    # Mock opening the history file into a CSV reader:
    mop = mock_open(read_data=load_fixture("node_history_samba_response.txt"))
    mop.return_value.__iter__ = lambda self: self
    mop.return_value.__next__ = lambda self: next(iter(self.readline, ""))

    with patch.object(
        tempfile,
        "NamedTemporaryFile",
        side_effect=[mock_measurements_tmp_file, mock_history_tmp_file],
    ), patch("smb.SMBConnection.SMBConnection.connect"), patch(
        "smb.SMBConnection.SMBConnection.listPath", return_value=[mock_history_file]
    ), patch(
        "smb.SMBConnection.SMBConnection.retrieveFile",
    ), patch(
        "smb.SMBConnection.SMBConnection.close"
    ), patch(
        "builtins.open", mop
    ):
        async with NodeSamba(TEST_NODE_IP_ADDRESS, TEST_NODE_PASSWORD) as node:
            history = await node.async_get_history(measurements_to_use=3)

        assert history["trends"] == {
            "aqi_cn": "flat",
            "aqi_us": "flat",
            "co2": "decreasing",
            "humidity": "decreasing",
            "pm0_1": "flat",
            "pm1_0": "decreasing",
            "pm2_5": "flat",
            "voc": "flat",
        }


@pytest.mark.asyncio
async def test_node_by_samba_get_file_errors():
    """Test various errors arising while getting a file via Samba."""
    node = NodeSamba(TEST_NODE_IP_ADDRESS, TEST_NODE_PASSWORD)

    with patch("smb.SMBConnection.SMBConnection.connect"), patch(
        "smb.SMBConnection.SMBConnection.retrieveFile",
        side_effect=smb.base.NotConnectedError,
    ):
        with pytest.raises(NodeProError):
            await node.async_connect()
            _ = await node.async_get_latest_measurements()

    with patch("smb.SMBConnection.SMBConnection.connect"), patch(
        "smb.SMBConnection.SMBConnection.retrieveFile", side_effect=smb.base.SMBTimeout,
    ):
        with pytest.raises(NodeProError):
            await node.async_connect()
            _ = await node.async_get_latest_measurements()

    with patch("smb.SMBConnection.SMBConnection.connect"), patch(
        "smb.SMBConnection.SMBConnection.retrieveFile",
        side_effect=smb.smb_structs.UnsupportedFeature,
    ):
        with pytest.raises(NodeProError):
            await node.async_connect()
            _ = await node.async_get_latest_measurements()

    with patch("smb.SMBConnection.SMBConnection.connect"), patch(
        "smb.SMBConnection.SMBConnection.retrieveFile",
        side_effect=smb.smb_structs.ProtocolError,
    ):
        with pytest.raises(NodeProError):
            await node.async_connect()
            _ = await node.async_get_latest_measurements()


@pytest.mark.asyncio
async def test_node_by_samba_history_errors():
    """Test various errors arising while getting history."""
    node = NodeSamba(TEST_NODE_IP_ADDRESS, TEST_NODE_PASSWORD)

    with patch("smb.SMBConnection.SMBConnection.connect"), patch(
        "smb.SMBConnection.SMBConnection.listPath",
        side_effect=smb.base.NotConnectedError,
    ):
        with pytest.raises(NodeProError):
            await node.async_connect()
            _ = await node.async_get_history()

    with patch("smb.SMBConnection.SMBConnection.connect"), patch(
        "smb.SMBConnection.SMBConnection.listPath", side_effect=smb.base.SMBTimeout,
    ):
        with pytest.raises(NodeProError):
            await node.async_connect()
            _ = await node.async_get_history()

    with patch("smb.SMBConnection.SMBConnection.connect"), patch(
        "smb.SMBConnection.SMBConnection.listPath",
        side_effect=smb.smb_structs.UnsupportedFeature,
    ):
        with pytest.raises(NodeProError):
            await node.async_connect()
            _ = await node.async_get_history()

    with patch("smb.SMBConnection.SMBConnection.connect"), patch(
        "smb.SMBConnection.SMBConnection.listPath",
        side_effect=smb.smb_structs.ProtocolError,
    ):
        with pytest.raises(NodeProError):
            await node.async_connect()
            _ = await node.async_get_history()


@pytest.mark.asyncio
async def test_node_by_samba_no_history_files():
    """Test the Node/Pro not having any history files where expected."""
    # Mock the tempfile that current measurements get loaded into:
    measurements_response = load_fixture("node_measurements_samba_response.json")
    mock_measurements_tmp_file = MagicMock()
    mock_measurements_tmp_file.read.return_value = measurements_response.encode()

    # Mock the history file that SMBConnection returns:
    mock_history_tmp_file = MagicMock()

    with patch.object(
        tempfile,
        "NamedTemporaryFile",
        side_effect=[mock_measurements_tmp_file, mock_history_tmp_file],
    ), patch("smb.SMBConnection.SMBConnection.connect"), patch(
        "smb.SMBConnection.SMBConnection.retrieveFile",
    ), patch(
        "smb.SMBConnection.SMBConnection.listPath", return_value=[]
    ), patch(
        "smb.SMBConnection.SMBConnection.close"
    ):
        with pytest.raises(NodeProError):
            async with NodeSamba(TEST_NODE_IP_ADDRESS, TEST_NODE_PASSWORD) as node:
                await node.async_get_history()
