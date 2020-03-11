"""Define tests for the "Supported" object."""
import aiohttp
import pytest

from pyairvisual import Client

from .common import TEST_API_KEY, TEST_CITY, TEST_COUNTRY, TEST_STATE, load_fixture


@pytest.mark.asyncio
async def test_cities(aresponses):
    """Test getting a list of supported cities."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/cities",
        "get",
        aresponses.Response(
            text=load_fixture("cities_response.json"),
            headers={"Content-Type": "application/json"},
            status=200,
        ),
    )

    async with aiohttp.ClientSession() as websession:
        client = Client(websession, api_key=TEST_API_KEY)
        data = await client.supported.cities(TEST_COUNTRY, TEST_STATE)
        assert len(data) == 27


@pytest.mark.asyncio
async def test_countries(aresponses):
    """Test getting a list of supported countries."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/countries",
        "get",
        aresponses.Response(
            text=load_fixture("countries_response.json"),
            headers={"Content-Type": "application/json"},
            status=200,
        ),
    )

    async with aiohttp.ClientSession() as websession:
        client = Client(websession, api_key=TEST_API_KEY)
        data = await client.supported.countries()
        assert len(data) == 79


@pytest.mark.asyncio
async def test_states(aresponses):
    """Test getting a list of supported states."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/states",
        "get",
        aresponses.Response(
            text=load_fixture("states_response.json"),
            headers={"Content-Type": "application/json"},
            status=200,
        ),
    )

    async with aiohttp.ClientSession() as websession:
        client = Client(websession, api_key=TEST_API_KEY)
        data = await client.supported.states(TEST_COUNTRY)
        assert len(data) == 6


@pytest.mark.asyncio
async def test_stations(aresponses):
    """Test getting a list of supported stations."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/stations",
        "get",
        aresponses.Response(
            text=load_fixture("stations_response.json"),
            headers={"Content-Type": "application/json"},
            status=200,
        ),
    )

    async with aiohttp.ClientSession() as websession:
        client = Client(websession, api_key=TEST_API_KEY)
        data = await client.supported.stations(TEST_CITY, TEST_STATE, TEST_COUNTRY)
        assert len(data) == 2
