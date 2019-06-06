"""Define tests for the "Data" object."""
# pylint: disable=redefined-outer-name,unused-import

import json

import aiohttp
import pytest

from pyairvisual import Client

from .const import (
    TEST_API_KEY,
    TEST_CITY,
    TEST_COUNTRY,
    TEST_LATITUDE,
    TEST_LONGITUDE,
    TEST_STATE,
    TEST_STATION_NAME,
)
from .fixtures.api import *


@pytest.mark.asyncio
async def test_aqi_ranking(aresponses, event_loop, fixture_ranking):
    """Test getting AQI ranking by city."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/city_ranking",
        "get",
        aresponses.Response(text=json.dumps(fixture_ranking), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = Client(websession, api_key=TEST_API_KEY)
        data = await client.api.ranking()

        assert len(data) == 3
        assert data[0]["city"] == "Portland"
        assert data[0]["state"] == "Oregon"
        assert data[0]["country"] == "USA"


@pytest.mark.asyncio
async def test_city_by_coordinates(aresponses, event_loop, fixture_city):
    """Test getting the nearest city by latitude and longitude."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/nearest_city",
        "get",
        aresponses.Response(text=json.dumps(fixture_city), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = Client(websession, api_key=TEST_API_KEY)
        data = await client.api.nearest_city(
            latitude=TEST_LATITUDE, longitude=TEST_LONGITUDE
        )

        assert data["city"] == "Los Angeles"
        assert data["state"] == "California"
        assert data["country"] == "USA"


@pytest.mark.asyncio
async def test_city_by_ip(aresponses, event_loop, fixture_city):
    """Test getting the nearest city by IP address."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/nearest_city",
        "get",
        aresponses.Response(text=json.dumps(fixture_city), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = Client(websession, api_key=TEST_API_KEY)
        data = await client.api.nearest_city()

        assert data["city"] == "Los Angeles"
        assert data["state"] == "California"
        assert data["country"] == "USA"


@pytest.mark.asyncio
async def test_city_by_name(aresponses, event_loop, fixture_city):
    """Test getting a city by its name."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/city",
        "get",
        aresponses.Response(text=json.dumps(fixture_city), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = Client(websession, api_key=TEST_API_KEY)
        data = await client.api.city(
            city=TEST_CITY, state=TEST_STATE, country=TEST_COUNTRY
        )

        assert data["city"] == "Los Angeles"
        assert data["state"] == "California"
        assert data["country"] == "USA"


@pytest.mark.asyncio
async def test_node(aresponses, event_loop, fixture_node):
    """Test getting a node."""
    aresponses.add(
        "www.airvisual.com",
        "/api/v2/node/12345",
        "get",
        aresponses.Response(text=json.dumps(fixture_node), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = Client(websession, api_key=TEST_API_KEY)
        data = await client.api.node("12345")

        assert data["current"]["tp"] == 2.3
        assert data["current"]["hm"] == 73
        assert data["current"]["p2"] == 35
        assert data["current"]["co"] == 479


@pytest.mark.asyncio
async def test_station_by_coordinates(aresponses, event_loop, fixture_station):
    """Test getting a station by latitude and longitude."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/nearest_station",
        "get",
        aresponses.Response(text=json.dumps(fixture_station), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = Client(websession, api_key=TEST_API_KEY)
        data = await client.api.nearest_station(
            latitude=TEST_LATITUDE, longitude=TEST_LONGITUDE
        )

        assert data["city"] == "Beijing"
        assert data["state"] == "Beijing"
        assert data["country"] == "China"


@pytest.mark.asyncio
async def test_station_by_ip(aresponses, event_loop, fixture_station):
    """Test getting a station by IP address."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/nearest_station",
        "get",
        aresponses.Response(text=json.dumps(fixture_station), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = Client(websession, api_key=TEST_API_KEY)
        data = await client.api.nearest_station()

        assert data["city"] == "Beijing"
        assert data["state"] == "Beijing"
        assert data["country"] == "China"


@pytest.mark.asyncio
async def test_station_by_name(aresponses, event_loop, fixture_station):
    """Test getting a station by location name."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/station",
        "get",
        aresponses.Response(text=json.dumps(fixture_station), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = Client(websession, api_key=TEST_API_KEY)
        data = await client.api.station(
            station=TEST_STATION_NAME,
            city=TEST_CITY,
            state=TEST_STATE,
            country=TEST_COUNTRY,
        )

        assert data["city"] == "Beijing"
        assert data["state"] == "Beijing"
        assert data["country"] == "China"
