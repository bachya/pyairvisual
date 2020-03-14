"""Define tests for the "Node" object."""
import aiohttp
import pytest

from pyairvisual import Client

from .common import TEST_API_KEY, load_fixture


@pytest.mark.asyncio
async def test_node(aresponses):
    """Test getting a node."""
    aresponses.add(
        "www.airvisual.com",
        "/api/v2/node/12345",
        "get",
        aresponses.Response(
            text=load_fixture("node_response.json"),
            headers={"Content-Type": "application/json"},
            status=200,
        ),
    )

    async with aiohttp.ClientSession() as websession:
        client = Client(websession, api_key=TEST_API_KEY)
        data = await client.node.from_cloud_api("12345")
        assert data["current"]["tp"] == 2.3
        assert data["current"]["hm"] == 73
        assert data["current"]["p2"] == 35
        assert data["current"]["co"] == 479
