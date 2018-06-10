"""Define tests for the client object."""
# pylint: disable=redefined-outer-name,unused-import

import aiohttp

from pyairvisual import Client

from .const import TEST_API_KEY


# pylint: disable=protected-access
async def test_create():
    """Test the creation of a client."""
    async with aiohttp.ClientSession() as websession:
        client = Client(TEST_API_KEY, websession)
        assert client._api_key == TEST_API_KEY
