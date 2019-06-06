"""Define tests for the "Supported" object."""
# pylint: disable=redefined-outer-name,unused-import

import json

import aiohttp
import pytest

from pyairvisual import Client

from .const import TEST_API_KEY, TEST_CITY, TEST_COUNTRY, TEST_STATE
from .fixtures.supported import *


@pytest.mark.asyncio
async def test_cities(aresponses, event_loop, fixture_cities):
    """Test getting a list of supported cities."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/cities",
        "get",
        aresponses.Response(text=json.dumps(fixture_cities), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = Client(websession, api_key=TEST_API_KEY)
        data = await client.supported.cities(TEST_COUNTRY, TEST_STATE)

        assert len(data) == 27


@pytest.mark.asyncio
async def test_countries(aresponses, event_loop, fixture_countries):
    """Test getting a list of supported countries."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/countries",
        "get",
        aresponses.Response(text=json.dumps(fixture_countries), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = Client(websession, api_key=TEST_API_KEY)
        data = await client.supported.countries()

        assert len(data) == 79


@pytest.mark.asyncio
async def test_states(aresponses, event_loop, fixture_states):
    """Test getting a list of supported states."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/states",
        "get",
        aresponses.Response(text=json.dumps(fixture_states), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = Client(websession, api_key=TEST_API_KEY)
        data = await client.supported.states(TEST_COUNTRY)

        assert len(data) == 6


@pytest.mark.asyncio
async def test_stations(aresponses, event_loop, fixture_stations):
    """Test getting a list of supported stations."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/stations",
        "get",
        aresponses.Response(text=json.dumps(fixture_stations), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = Client(websession, api_key=TEST_API_KEY)
        data = await client.supported.stations(TEST_CITY, TEST_STATE, TEST_COUNTRY)

        assert len(data) == 2
