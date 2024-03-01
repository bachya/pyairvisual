"""Define tests for API requests and responses."""

import json

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from pyairvisual import CloudAPI
from tests.common import (
    TEST_API_KEY,
    TEST_CITY,
    TEST_COUNTRY,
    TEST_LATITUDE,
    TEST_LONGITUDE,
    TEST_NODE_ID,
    TEST_STATE,
    TEST_STATION_NAME,
)


@pytest.mark.asyncio
async def test_aqi_ranking(
    aresponses: ResponsesMockServer, city_ranking_response: str
) -> None:
    """Test getting AQI ranking by city.

    Args:
        aresponses: An aresponses server.
        city_ranking_response: An API response payload.
    """
    aresponses.add(
        "api.airvisual.com",
        "/v2/city_ranking",
        "get",
        response=aiohttp.web_response.json_response(
            json.loads(city_ranking_response), status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        cloud_api = CloudAPI(TEST_API_KEY, session=session)
        data = await cloud_api.air_quality.ranking()
        assert len(data) == 3
        assert data[0]["city"] == "Portland"
        assert data[0]["state"] == "Oregon"
        assert data[0]["country"] == "USA"

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_cities(aresponses: ResponsesMockServer, cities_response: str) -> None:
    """Test getting a list of supported cities.

    Args:
        aresponses: An aresponses server.
        cities_response: An API response payload.
    """
    aresponses.add(
        "api.airvisual.com",
        "/v2/cities",
        "get",
        response=aiohttp.web_response.json_response(
            json.loads(cities_response), status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        cloud_api = CloudAPI(TEST_API_KEY, session=session)
        data = await cloud_api.supported.cities(TEST_COUNTRY, TEST_STATE)
        assert len(data) == 27

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_city_by_coordinates(
    aresponses: ResponsesMockServer, city_response: str
) -> None:
    """Test getting the nearest city by latitude and longitude.

    Args:
        aresponses: An aresponses server.
        city_response: An API response payload.
    """
    aresponses.add(
        "api.airvisual.com",
        "/v2/nearest_city",
        "get",
        response=aiohttp.web_response.json_response(
            json.loads(city_response), status=200
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

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_city_by_ip(aresponses: ResponsesMockServer, city_response: str) -> None:
    """Test getting the nearest city by IP address.

    Args:
        aresponses: An aresponses server.
        city_response: An API response payload.
    """
    aresponses.add(
        "api.airvisual.com",
        "/v2/nearest_city",
        "get",
        response=aiohttp.web_response.json_response(
            json.loads(city_response), status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        cloud_api = CloudAPI(TEST_API_KEY, session=session)
        data = await cloud_api.air_quality.nearest_city()
        assert data["city"] == "Los Angeles"
        assert data["state"] == "California"
        assert data["country"] == "USA"

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_city_by_name(
    aresponses: ResponsesMockServer, city_response: str
) -> None:
    """Test getting a city by its name.

    Args:
        aresponses: An aresponses server.
        city_response: An API response payload.
    """
    aresponses.add(
        "api.airvisual.com",
        "/v2/city",
        "get",
        response=aiohttp.web_response.json_response(
            json.loads(city_response), status=200
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

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_countries(
    aresponses: ResponsesMockServer, countries_response: str
) -> None:
    """Test getting a list of supported countries.

    Args:
        aresponses: An aresponses server.
        countries_response: An API response payload.
    """
    aresponses.add(
        "api.airvisual.com",
        "/v2/countries",
        "get",
        response=aiohttp.web_response.json_response(
            json.loads(countries_response), status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        cloud_api = CloudAPI(TEST_API_KEY, session=session)
        data = await cloud_api.supported.countries()
        assert len(data) == 79

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_no_explicit_client_session(
    aresponses: ResponsesMockServer, city_ranking_response: str
) -> None:
    """Test not explicitly providing an aiohttp ClientSession.

    Args:
        aresponses: An aresponses server.
        city_ranking_response: An API response payload.
    """
    aresponses.add(
        "api.airvisual.com",
        "/v2/city_ranking",
        "get",
        response=aiohttp.web_response.json_response(
            json.loads(city_ranking_response), status=200
        ),
    )

    cloud_api = CloudAPI(TEST_API_KEY)
    data = await cloud_api.air_quality.ranking()
    assert len(data) == 3
    assert data[0]["city"] == "Portland"
    assert data[0]["state"] == "Oregon"
    assert data[0]["country"] == "USA"

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_node_by_id(
    aresponses: ResponsesMockServer, node_by_id_response: str
) -> None:
    """Test getting a node's info by its ID from the cloud API.

    Args:
        aresponses: An aresponses server.
        node_by_id_response: An API response payload.
    """
    aresponses.add(
        "www.airvisual.com",
        "/api/v2/node/12345",
        "get",
        response=aiohttp.web_response.json_response(
            json.loads(node_by_id_response), status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        cloud_api = CloudAPI(TEST_API_KEY, session=session)
        data = await cloud_api.node.get_by_node_id(TEST_NODE_ID)
        assert data["current"]["tp"] == 2.3
        assert data["current"]["hm"] == 73
        assert data["current"]["p2"] == 35
        assert data["current"]["co"] == 479

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_states(aresponses: ResponsesMockServer, states_response: str) -> None:
    """Test getting a list of supported states.

    Args:
        aresponses: An aresponses server.
        states_response: An API response payload.
    """
    aresponses.add(
        "api.airvisual.com",
        "/v2/states",
        "get",
        response=aiohttp.web_response.json_response(
            json.loads(states_response), status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        cloud_api = CloudAPI(TEST_API_KEY, session=session)
        data = await cloud_api.supported.states(TEST_COUNTRY)
        assert len(data) == 6

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_station_by_coordinates(
    aresponses: ResponsesMockServer, station_response: str
) -> None:
    """Test getting a station by latitude and longitude.

    Args:
        aresponses: An aresponses server.
        station_response: An API response payload.
    """
    aresponses.add(
        "api.airvisual.com",
        "/v2/nearest_station",
        "get",
        response=aiohttp.web_response.json_response(
            json.loads(station_response), status=200
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

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_station_by_ip(
    aresponses: ResponsesMockServer, station_response: str
) -> None:
    """Test getting a station by IP address.

    Args:
        aresponses: An aresponses server.
        station_response: An API response payload.
    """
    aresponses.add(
        "api.airvisual.com",
        "/v2/nearest_station",
        "get",
        response=aiohttp.web_response.json_response(
            json.loads(station_response), status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        cloud_api = CloudAPI(TEST_API_KEY, session=session)
        data = await cloud_api.air_quality.nearest_station()
        assert data["city"] == "Beijing"
        assert data["state"] == "Beijing"
        assert data["country"] == "China"

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_station_by_name(
    aresponses: ResponsesMockServer, station_response: str
) -> None:
    """Test getting a station by location name.

    Args:
        aresponses: An aresponses server.
        station_response: An API response payload.
    """
    aresponses.add(
        "api.airvisual.com",
        "/v2/station",
        "get",
        response=aiohttp.web_response.json_response(
            json.loads(station_response), status=200
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

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_stations(
    aresponses: ResponsesMockServer, stations_response: str
) -> None:
    """Test getting a list of supported stations.

    Args:
        aresponses: An aresponses server.
        stations_response: An API response payload.
    """
    aresponses.add(
        "api.airvisual.com",
        "/v2/stations",
        "get",
        response=aiohttp.web_response.json_response(
            json.loads(stations_response), status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        cloud_api = CloudAPI(TEST_API_KEY, session=session)
        data = await cloud_api.supported.stations(TEST_CITY, TEST_STATE, TEST_COUNTRY)
        assert len(data) == 2

    aresponses.assert_plan_strictly_followed()
