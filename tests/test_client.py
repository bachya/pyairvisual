"""Define tests for the client object."""
import aiohttp

from pyairvisual import Client

from .common import TEST_API_KEY


async def test_create():
    """Test the creation of a client."""
    async with aiohttp.ClientSession() as websession:
        client = Client(websession, api_key=TEST_API_KEY)
        assert client._api_key == TEST_API_KEY  # pylint: disable=protected-access
