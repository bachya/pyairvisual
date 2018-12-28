"""Define tests for various errors."""
# pylint: disable=redefined-outer-name,unused-import

import json

import aiohttp
import pytest

from pyairvisual import Client
from pyairvisual.errors import AirVisualError, KeyExpiredError, RequestError

from .const import TEST_API_KEY


@pytest.fixture(scope='module')
def fixture_generic_error():
    """Return a response when the API key is expired."""
    return {"status": "fail", "data": {"message": "unknown_key"}}


@pytest.fixture(scope='module')
def fixture_key_expired():
    """Return a response when the API key is expired."""
    return {"status": "fail", "data": {"message": "api_key_expired"}}


@pytest.mark.asyncio
async def test_api_key_expired(aresponses, event_loop, fixture_key_expired):
    """Test that the proper error is raised when the API is expired."""
    aresponses.add(
        'api.airvisual.com', '/v2/nearest_city', 'get',
        aresponses.Response(text=json.dumps(fixture_key_expired), status=401))

    with pytest.raises(KeyExpiredError):
        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = Client(TEST_API_KEY, websession)
            await client.api.nearest_city()


@pytest.mark.asyncio
async def test_generic_error(aresponses, event_loop, fixture_generic_error):
    """Test that a generic error is raised appropriately."""
    aresponses.add(
        'api.airvisual.com', '/v2/nearest_city', 'get',
        aresponses.Response(
            text=json.dumps(fixture_generic_error), status=401))

    with pytest.raises(AirVisualError):
        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = Client(TEST_API_KEY, websession)
            await client.api.nearest_city()
