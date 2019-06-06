"""Define tests for various errors."""
# pylint: disable=redefined-outer-name,unused-import

import json

import aiohttp
import pytest

from pyairvisual import Client
from pyairvisual.errors import (
    AirVisualError,
    InvalidKeyError,
    KeyExpiredError,
    LimitReachedError,
    NoStationError,
    NotFoundError,
    UnauthorizedError,
)

from .const import TEST_API_KEY
from .fixtures.errors import *


@pytest.mark.asyncio
async def test_api_key_expired(aresponses, event_loop, fixture_key_expired):
    """Test that the proper error is raised when the API is expired."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/nearest_city",
        "get",
        aresponses.Response(text=json.dumps(fixture_key_expired), status=401),
    )

    with pytest.raises(KeyExpiredError):
        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = Client(websession, api_key=TEST_API_KEY)
            await client.api.nearest_city()


@pytest.mark.asyncio
async def test_call_limit_reached(aresponses, event_loop, fixture_limit_reached):
    """Test that the proper error is raised when the call limit is reached."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/nearest_city",
        "get",
        aresponses.Response(text=json.dumps(fixture_limit_reached), status=401),
    )

    with pytest.raises(LimitReachedError):
        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = Client(websession, api_key=TEST_API_KEY)
            await client.api.nearest_city()


@pytest.mark.asyncio
async def test_city_not_found(aresponses, event_loop, fixture_city_not_found):
    """Test that the proper error is raised when a city cannot be found."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/nearest_city",
        "get",
        aresponses.Response(text=json.dumps(fixture_city_not_found), status=401),
    )

    with pytest.raises(NotFoundError):
        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = Client(websession, api_key=TEST_API_KEY)
            await client.api.nearest_city()


@pytest.mark.asyncio
async def test_generic_error(aresponses, event_loop, fixture_generic_error):
    """Test that a generic error is raised appropriately."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/nearest_city",
        "get",
        aresponses.Response(text=json.dumps(fixture_generic_error), status=401),
    )

    with pytest.raises(AirVisualError):
        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = Client(websession, api_key=TEST_API_KEY)
            await client.api.nearest_city()


@pytest.mark.asyncio
async def test_incorrect_api_key(aresponses, event_loop, fixture_incorrect_api_key):
    """Test that the proper error is raised with an incorrect API key."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/nearest_city",
        "get",
        aresponses.Response(text=json.dumps(fixture_incorrect_api_key), status=401),
    )

    with pytest.raises(InvalidKeyError):
        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = Client(websession, api_key=TEST_API_KEY)
            await client.api.nearest_city()


@pytest.mark.asyncio
async def test_no_nearest_station(aresponses, event_loop, fixture_no_nearest_station):
    """Test that the proper error is raised when no station is found."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/nearest_station",
        "get",
        aresponses.Response(text=json.dumps(fixture_no_nearest_station), status=401),
    )

    with pytest.raises(NoStationError):
        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = Client(websession, api_key=TEST_API_KEY)
            await client.api.nearest_station()


@pytest.mark.asyncio
async def test_node_not_found(aresponses, event_loop, fixture_no_node):
    """Test that the proper error is raised when no Pro node is found."""
    aresponses.add(
        "www.airvisual.com",
        "/api/v2/node/12345",
        "get",
        aresponses.Response(text=json.dumps(fixture_no_node), status=200),
    )

    with pytest.raises(NotFoundError):
        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = Client(websession, api_key=TEST_API_KEY)
            await client.api.node("12345")


@pytest.mark.asyncio
async def test_permission_denied(aresponses, event_loop, fixture_permission_denied):
    """Test that the proper error is raised when permission is denied."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/nearest_station",
        "get",
        aresponses.Response(text=json.dumps(fixture_permission_denied), status=401),
    )

    with pytest.raises(UnauthorizedError):
        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = Client(websession, api_key=TEST_API_KEY)
            await client.api.nearest_station()
