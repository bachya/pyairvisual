"""Define tests for the "Data" object."""
import aiohttp
import pytest

from pyairvisual import Client

from .common import (
    TEST_API_KEY,
    TEST_CITY,
    TEST_COUNTRY,
    TEST_LATITUDE,
    TEST_LONGITUDE,
    TEST_STATE,
    TEST_STATION_NAME,
    load_fixture,
)


@pytest.mark.asyncio
async def test_aqi_ranking(aresponses):
    """Test getting AQI ranking by city."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/city_ranking",
        "get",
        aresponses.Response(
            text=load_fixture("city_ranking_response.json"),
            headers={"Content-Type": "application/json"},
            status=200,
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(api_key=TEST_API_KEY, session=session)
        data = await client.api.ranking()
        assert len(data) == 3
        assert data[0]["city"] == "Portland"
        assert data[0]["state"] == "Oregon"
        assert data[0]["country"] == "USA"


@pytest.mark.asyncio
async def test_city_by_coordinates(aresponses):
    """Test getting the nearest city by latitude and longitude."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/nearest_city",
        "get",
        aresponses.Response(
            text=load_fixture("city_response.json"),
            headers={"Content-Type": "application/json"},
            status=200,
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(api_key=TEST_API_KEY, session=session)
        data = await client.api.nearest_city(
            latitude=TEST_LATITUDE, longitude=TEST_LONGITUDE
        )
        assert data["city"] == "Los Angeles"
        assert data["state"] == "California"
        assert data["country"] == "USA"


@pytest.mark.asyncio
async def test_city_by_ip(aresponses):
    """Test getting the nearest city by IP address."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/nearest_city",
        "get",
        aresponses.Response(
            text=load_fixture("city_response.json"),
            headers={"Content-Type": "application/json"},
            status=200,
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(api_key=TEST_API_KEY, session=session)
        data = await client.api.nearest_city()
        assert data["city"] == "Los Angeles"
        assert data["state"] == "California"
        assert data["country"] == "USA"


@pytest.mark.asyncio
async def test_city_by_name(aresponses):
    """Test getting a city by its name."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/city",
        "get",
        aresponses.Response(
            text=load_fixture("city_response.json"),
            headers={"Content-Type": "application/json"},
            status=200,
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(api_key=TEST_API_KEY, session=session)
        data = await client.api.city(
            city=TEST_CITY, state=TEST_STATE, country=TEST_COUNTRY
        )

        assert data["city"] == "Los Angeles"
        assert data["state"] == "California"
        assert data["country"] == "USA"


@pytest.mark.asyncio
async def test_no_explicit_client_session(aresponses):
    """Test not explicitly providing an aiohttp ClientSession."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/city_ranking",
        "get",
        aresponses.Response(
            text=load_fixture("city_ranking_response.json"),
            headers={"Content-Type": "application/json"},
            status=200,
        ),
    )

    client = Client(api_key=TEST_API_KEY)
    data = await client.api.ranking()
    assert len(data) == 3
    assert data[0]["city"] == "Portland"
    assert data[0]["state"] == "Oregon"
    assert data[0]["country"] == "USA"


@pytest.mark.asyncio
async def test_station_by_coordinates(aresponses):
    """Test getting a station by latitude and longitude."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/nearest_station",
        "get",
        aresponses.Response(
            text=load_fixture("station_response.json"),
            headers={"Content-Type": "application/json"},
            status=200,
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(api_key=TEST_API_KEY, session=session)
        data = await client.api.nearest_station(
            latitude=TEST_LATITUDE, longitude=TEST_LONGITUDE
        )
        assert data["city"] == "Beijing"
        assert data["state"] == "Beijing"
        assert data["country"] == "China"


@pytest.mark.asyncio
async def test_station_by_ip(aresponses):
    """Test getting a station by IP address."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/nearest_station",
        "get",
        aresponses.Response(
            text=load_fixture("station_response.json"),
            headers={"Content-Type": "application/json"},
            status=200,
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(api_key=TEST_API_KEY, session=session)
        data = await client.api.nearest_station()
        assert data["city"] == "Beijing"
        assert data["state"] == "Beijing"
        assert data["country"] == "China"


@pytest.mark.asyncio
async def test_station_by_name(aresponses):
    """Test getting a station by location name."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/station",
        "get",
        aresponses.Response(
            text=load_fixture("station_response.json"),
            headers={"Content-Type": "application/json"},
            status=200,
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(api_key=TEST_API_KEY, session=session)
        data = await client.api.station(
            station=TEST_STATION_NAME,
            city=TEST_CITY,
            state=TEST_STATE,
            country=TEST_COUNTRY,
        )
        assert data["city"] == "Beijing"
        assert data["state"] == "Beijing"
        assert data["country"] == "China"
