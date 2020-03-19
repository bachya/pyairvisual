"""Define tests for the "Node" object."""
import tempfile
from unittest.mock import MagicMock, PropertyMock, mock_open

import aiohttp
from asynctest import patch
import pytest
import smb

from pyairvisual import Client
from pyairvisual.errors import NodeProError
from pyairvisual.node import NodeSamba

from .common import TEST_NODE_ID, TEST_NODE_IP_ADDRESS, TEST_NODE_PASSWORD, load_fixture


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

    async with aiohttp.ClientSession() as websession:
        client = Client(websession)
        data = await client.node.from_cloud_api(TEST_NODE_ID)
        assert data["current"]["tp"] == 2.3
        assert data["current"]["hm"] == 73
        assert data["current"]["p2"] == 35
        assert data["current"]["co"] == 479


@pytest.mark.asyncio
async def test_node_by_samba():
    """Test getting a node's info over the local network (via Samba)."""
    async with aiohttp.ClientSession() as websession:
        client = Client(websession)

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
            data = await client.node.from_samba(
                TEST_NODE_IP_ADDRESS, TEST_NODE_PASSWORD
            )

            assert data["current"]["measurements"]["co2"] == "442"
            assert data["current"]["measurements"]["humidity"] == "35"
            assert data["current"]["measurements"]["pm0_1"] == "3"
            assert data["current"]["measurements"]["pm1_0"] == "4"
            assert data["current"]["measurements"]["aqi_cn"] == "6"
            assert data["current"]["measurements"]["aqi_us"] == "17"
            assert data["current"]["measurements"]["pm2_5"] == "4.0"
            assert data["current"]["measurements"]["temperature_C"] == "19.3"
            assert data["current"]["measurements"]["temperature_F"] == "66.8"
            assert data["current"]["measurements"]["voc"] == "-1"

            assert len(data["history"]) == 7

            assert data["trends"] == {
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
        with pytest.raises(NodeProError):
            await node.async_connect()

    with patch(
        "smb.SMBConnection.SMBConnection.connect", side_effect=smb.base.SMBTimeout,
    ):
        with pytest.raises(NodeProError):
            await node.async_connect()


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
async def test_node_by_samba_no_history_or_trends():
    """Test getting a node's info over the local network without history or trends."""
    async with aiohttp.ClientSession() as websession:
        client = Client(websession)

        # Mock the tempfile that current measurements get loaded into:
        measurements_response = load_fixture("node_measurements_samba_response.json")
        mock_measurements_tmp_file = MagicMock()
        mock_measurements_tmp_file.read.return_value = measurements_response.encode()

        with patch.object(
            tempfile, "NamedTemporaryFile", return_value=mock_measurements_tmp_file,
        ), patch("smb.SMBConnection.SMBConnection.connect"), patch(
            "smb.SMBConnection.SMBConnection.retrieveFile",
        ), patch(
            "smb.SMBConnection.SMBConnection.close"
        ):
            data = await client.node.from_samba(
                TEST_NODE_IP_ADDRESS,
                TEST_NODE_PASSWORD,
                include_history=False,
                include_trends=False,
            )

            assert data["current"] != {}
            assert not data.get("history")
            assert not data.get("trends")


@pytest.mark.asyncio
async def test_node_by_samba_no_history_files():
    """Test the Node/Pro not having any history files where expected."""
    async with aiohttp.ClientSession() as websession:
        client = Client(websession)

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
                _ = await client.node.from_samba(
                    TEST_NODE_IP_ADDRESS, TEST_NODE_PASSWORD
                )
