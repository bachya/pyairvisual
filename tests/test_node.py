"""Define tests for the "Node" object."""
import tempfile
from unittest.mock import MagicMock

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

        samba_response = load_fixture("node_by_samba_response.json")
        mock_named_temporary_file = MagicMock()
        mock_named_temporary_file.read.return_value = samba_response.encode()

        with patch("smb.SMBConnection.SMBConnection.connect"), patch(
            "smb.SMBConnection.SMBConnection.retrieveFile"
        ), patch("smb.SMBConnection.SMBConnection.close"), patch.object(
            tempfile, "NamedTemporaryFile", return_value=mock_named_temporary_file
        ):
            data = await client.node.from_samba(
                TEST_NODE_IP_ADDRESS, TEST_NODE_PASSWORD
            )
            assert data["measurements"][0]["co2_ppm"] == "442"
            assert data["measurements"][0]["humidity_RH"] == "35"
            assert data["measurements"][0]["pm01_ugm3"] == "3"
            assert data["measurements"][0]["pm10_ugm3"] == "4"
            assert data["measurements"][0]["pm25_AQICN"] == "6"
            assert data["measurements"][0]["pm25_AQIUS"] == "17"
            assert data["measurements"][0]["pm25_ugm3"] == "4.0"
            assert data["measurements"][0]["temperature_C"] == "19.3"
            assert data["measurements"][0]["temperature_F"] == "66.8"
            assert data["measurements"][0]["voc_ppb"] == "-1"


@pytest.mark.asyncio
async def test_node_by_samba_connect_failure(caplog):
    """Test getting a node's info over the local network (via Samba)."""
    async with aiohttp.ClientSession() as websession:
        client = Client(websession)

        samba_response = load_fixture("node_by_samba_response.json")
        mock_named_temporary_file = MagicMock()
        mock_named_temporary_file.read.return_value = samba_response.encode()

        with pytest.raises(Exception):
            with patch(
                "smb.SMBConnection.SMBConnection.connect", side_effect=Exception
            ):
                _ = await client.node.from_samba(
                    TEST_NODE_IP_ADDRESS, TEST_NODE_PASSWORD
                )
            assert any(
                "Error while connecting to unit" in e.message for e in caplog.records
            )
