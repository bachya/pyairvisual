"""Define tests for the AirVisual Cloud API."""
import aiohttp
import pytest

from pyairvisual import CloudAPI

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
        cloud_api = CloudAPI(TEST_API_KEY, session=session)
        data = await cloud_api.air_quality.ranking()
        assert len(data) == 3
        assert data[0]["city"] == "Portland"
        assert data[0]["state"] == "Oregon"
        assert data[0]["country"] == "USA"


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

    async with aiohttp.ClientSession() as session:
        cloud_api = CloudAPI(TEST_API_KEY, session=session)
        data = await cloud_api.supported.cities(TEST_COUNTRY, TEST_STATE)
        assert len(data) == 27


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
        cloud_api = CloudAPI(TEST_API_KEY, session=session)
        data = await cloud_api.air_quality.nearest_city(
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
        cloud_api = CloudAPI(TEST_API_KEY, session=session)
        data = await cloud_api.air_quality.nearest_city()
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
        cloud_api = CloudAPI(TEST_API_KEY, session=session)
        data = await cloud_api.air_quality.city(
            city=TEST_CITY, state=TEST_STATE, country=TEST_COUNTRY
        )

        assert data["city"] == "Los Angeles"
        assert data["state"] == "California"
        assert data["country"] == "USA"


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

    async with aiohttp.ClientSession() as session:
        cloud_api = CloudAPI(TEST_API_KEY, session=session)
        data = await cloud_api.supported.countries()
        assert len(data) == 79


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

    cloud_api = CloudAPI(TEST_API_KEY)
    data = await cloud_api.air_quality.ranking()
    assert len(data) == 3
    assert data[0]["city"] == "Portland"
    assert data[0]["state"] == "Oregon"
    assert data[0]["country"] == "USA"


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

    async with aiohttp.ClientSession() as session:
        cloud_api = CloudAPI(TEST_API_KEY, session=session)
        data = await cloud_api.supported.states(TEST_COUNTRY)
        assert len(data) == 6


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
        cloud_api = CloudAPI(TEST_API_KEY, session=session)
        data = await cloud_api.air_quality.nearest_station(
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
        cloud_api = CloudAPI(TEST_API_KEY, session=session)
        data = await cloud_api.air_quality.nearest_station()
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
        cloud_api = CloudAPI(TEST_API_KEY, session=session)
        data = await cloud_api.air_quality.station(
            station=TEST_STATION_NAME,
            city=TEST_CITY,
            state=TEST_STATE,
            country=TEST_COUNTRY,
        )
        assert data["city"] == "Beijing"
        assert data["state"] == "Beijing"
        assert data["country"] == "China"


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

    async with aiohttp.ClientSession() as session:
        cloud_api = CloudAPI(TEST_API_KEY, session=session)
        data = await cloud_api.supported.stations(TEST_CITY, TEST_STATE, TEST_COUNTRY)
        assert len(data) == 2
