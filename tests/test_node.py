"""Define tests for the "Node" object."""
import tempfile
from unittest.mock import MagicMock, PropertyMock, mock_open

import aiohttp
from asynctest import patch
import pytest

from pyairvisual import Client

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
            assert data["current"]["measurements"][0]["co2_ppm"] == "442"
            assert data["current"]["measurements"][0]["humidity_RH"] == "35"
            assert data["current"]["measurements"][0]["pm01_ugm3"] == "3"
            assert data["current"]["measurements"][0]["pm10_ugm3"] == "4"
            assert data["current"]["measurements"][0]["pm25_AQICN"] == "6"
            assert data["current"]["measurements"][0]["pm25_AQIUS"] == "17"
            assert data["current"]["measurements"][0]["pm25_ugm3"] == "4.0"
            assert data["current"]["measurements"][0]["temperature_C"] == "19.3"
            assert data["current"]["measurements"][0]["temperature_F"] == "66.8"
            assert data["current"]["measurements"][0]["voc_ppb"] == "-1"


# @pytest.mark.asyncio
# async def test_node_by_samba_connect_failure(caplog):
#     """Test getting a node's info over the local network (via Samba)."""
#     async with aiohttp.ClientSession() as websession:
#         client = Client(websession)

#         measurements_response = load_fixture("node_measurements_samba_response.json")
#         mock_measurements_tmp_file = MagicMock()
#         mock_measurements_tmp_file.read.return_value = measurements_response.encode()

#         with pytest.raises(Exception):
#             with patch(
#                 "smb.SMBConnection.SMBConnection.connect", side_effect=Exception
#             ):
#                 _ = await client.node.from_samba(
#                     TEST_NODE_IP_ADDRESS, TEST_NODE_PASSWORD
#                 )
#             assert any(
#                 "Error while connecting to unit" in e.message for e in caplog.records
#             )
