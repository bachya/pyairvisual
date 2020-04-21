"""Define tests for various errors."""
import aiohttp
import pytest

from pyairvisual import Client
from pyairvisual.errors import (
    AirVisualError,
    InvalidKeyError,
    KeyExpiredError,
    LimitReachedError,
    NodeProError,
    NoStationError,
    NotFoundError,
    UnauthorizedError,
)

from .common import TEST_API_KEY, load_fixture


@pytest.mark.asyncio
async def test_api_key_expired(aresponses):
    """Test that the proper error is raised when the API is expired."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/nearest_city",
        "get",
        aresponses.Response(
            text=load_fixture("error_key_expired_response.json"),
            headers={"Content-Type": "application/json"},
            status=401,
        ),
    )

    with pytest.raises(KeyExpiredError):
        async with aiohttp.ClientSession() as session:
            client = Client(api_key=TEST_API_KEY, session=session)
            await client.api.nearest_city()


@pytest.mark.asyncio
async def test_call_limit_reached(aresponses):
    """Test that the proper error is raised when the call limit is reached."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/nearest_city",
        "get",
        aresponses.Response(
            text=load_fixture("error_limit_reached_response.json"),
            headers={"Content-Type": "application/json"},
            status=401,
        ),
    )

    with pytest.raises(LimitReachedError):
        async with aiohttp.ClientSession() as session:
            client = Client(api_key=TEST_API_KEY, session=session)
            await client.api.nearest_city()


@pytest.mark.asyncio
async def test_city_not_found(aresponses):
    """Test that the proper error is raised when a city cannot be found."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/nearest_city",
        "get",
        aresponses.Response(
            text=load_fixture("error_city_not_found_response.json"),
            headers={"Content-Type": "application/json"},
            status=401,
        ),
    )

    with pytest.raises(NotFoundError):
        async with aiohttp.ClientSession() as session:
            client = Client(api_key=TEST_API_KEY, session=session)
            await client.api.nearest_city()


@pytest.mark.asyncio
async def test_generic_error(aresponses):
    """Test that a generic error is raised appropriately."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/nearest_city",
        "get",
        aresponses.Response(
            text=load_fixture("error_generic_response.json"),
            headers={"Content-Type": "application/json"},
            status=401,
        ),
    )

    with pytest.raises(AirVisualError):
        async with aiohttp.ClientSession() as session:
            client = Client(api_key=TEST_API_KEY, session=session)
            await client.api.nearest_city()


@pytest.mark.asyncio
async def test_incorrect_api_key(aresponses):
    """Test that the proper error is raised with an incorrect API key."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/nearest_city",
        "get",
        aresponses.Response(
            text=load_fixture("error_incorrect_api_key_response.json"),
            headers={"Content-Type": "application/json"},
            status=401,
        ),
    )

    with pytest.raises(InvalidKeyError):
        async with aiohttp.ClientSession() as session:
            client = Client(api_key=TEST_API_KEY, session=session)
            await client.api.nearest_city()


@pytest.mark.asyncio
async def test_no_nearest_station(aresponses):
    """Test that the proper error is raised when no station is found."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/nearest_station",
        "get",
        aresponses.Response(
            text=load_fixture("error_no_nearest_station_response.json"),
            headers={"Content-Type": "application/json"},
            status=401,
        ),
    )

    with pytest.raises(NoStationError):
        async with aiohttp.ClientSession() as session:
            client = Client(api_key=TEST_API_KEY, session=session)
            await client.api.nearest_station()


@pytest.mark.asyncio
async def test_node_not_found(aresponses):
    """Test that the proper error is raised when no Pro node is found."""
    aresponses.add(
        "www.airvisual.com",
        "/api/v2/node/12345",
        "get",
        aresponses.Response(
            text='"node not found"',
            headers={"Content-Type": "application/json"},
            status=200,
        ),
    )

    with pytest.raises(NodeProError):
        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.node.from_cloud_api("12345")


@pytest.mark.asyncio
async def test_non_json_response(aresponses):
    """Test that the proper error is raised when the response text isn't JSON."""
    aresponses.add(
        "www.airvisual.com",
        "/api/v2/node/12345",
        "get",
        aresponses.Response(
            text="This is a valid response, but it isn't JSON.",
            headers={"Content-Type": "application/json"},
            status=200,
        ),
    )

    with pytest.raises(AirVisualError):
        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.node.from_cloud_api("12345")


@pytest.mark.asyncio
async def test_permission_denied(aresponses):
    """Test that the proper error is raised when permission is denied."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/nearest_station",
        "get",
        aresponses.Response(
            text=load_fixture("error_permission_denied_response.json"),
            headers={"Content-Type": "application/json"},
            status=401,
        ),
    )

    with pytest.raises(UnauthorizedError):
        async with aiohttp.ClientSession() as session:
            client = Client(api_key=TEST_API_KEY, session=session)
            await client.api.nearest_station()
