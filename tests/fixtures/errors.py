"""Define fixtures for the various errors."""
import pytest


@pytest.fixture()
def fixture_city_not_found():
    """Return a response when a city can't be found."""
    return {"status": "fail", "data": {"message": "city_not_found"}}


@pytest.fixture()
def fixture_generic_error():
    """Return an unknown/generic error response."""
    return {"status": "fail", "data": {"message": "unknown_key"}}


@pytest.fixture()
def fixture_incorrect_api_key():
    """Return a response when an API key is invalid."""
    return {"status": "fail", "data": {"message": "incorrect_api_key"}}


@pytest.fixture()
def fixture_key_expired():
    """Return a response when the API key is expired."""
    return {"status": "fail", "data": {"message": "api_key_expired"}}


@pytest.fixture()
def fixture_limit_reached():
    """Return a response when the API limit is reached."""
    return {"status": "fail", "data": {"message": "call_limit_reached"}}


@pytest.fixture()
def fixture_no_nearest_station():
    """Return a response when the nearest station cannot be determined."""
    return {"status": "fail", "data": {"message": "no_nearest_station"}}


@pytest.fixture()
def fixture_no_node():
    """Return a response when a node cannot be found."""
    return "node not found"


@pytest.fixture()
def fixture_permission_denied():
    """Return a response when permission is denied."""
    return {"status": "fail", "data": {"message": "permission_denied"}}
