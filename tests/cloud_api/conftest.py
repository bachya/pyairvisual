"""Define dynamic test fixtures."""

import pytest

from tests.common import load_fixture


@pytest.fixture(name="cities_response", scope="session")
def cities_response_fixture() -> str:
    """Define a fixture for response data containing a list of cities.

    Returns:
        An API response payload.
    """
    return load_fixture("cities_response.json")


@pytest.fixture(name="city_response", scope="session")
def city_response_fixture() -> str:
    """Define a fixture for response data containing a single city.

    Returns:
        An API response payload.
    """
    return load_fixture("city_response.json")


@pytest.fixture(name="city_ranking_response", scope="session")
def city_ranking_response_fixture() -> str:
    """Define a fixture for response data containing city ranking information.

    Returns:
        An API response payload.
    """
    return load_fixture("city_ranking_response.json")


@pytest.fixture(name="countries_response", scope="session")
def countries_response_fixture() -> str:
    """Define a fixture for response data containing a list of countries.

    Returns:
        An API response payload.
    """
    return load_fixture("countries_response.json")


@pytest.fixture(name="error_city_not_found_response", scope="session")
def error_city_not_found_response_fixture() -> str:
    """Define a fixture for error response data (city not found).

    Returns:
        An API response payload.
    """
    return load_fixture("error_city_not_found_response.json")


@pytest.fixture(name="error_forbidden_response", scope="session")
def error_forbidden_response_fixture() -> str:
    """Define a fixture for error response data (forbidden).

    Returns:
        An API response payload.
    """
    return load_fixture("error_forbidden_response.json")


@pytest.fixture(name="error_generic_response", scope="session")
def error_generic_response_fixture() -> str:
    """Define a fixture for error response data (generic).

    Returns:
        An API response payload.
    """
    return load_fixture("error_generic_response.json")


@pytest.fixture(name="error_incorrect_api_key_response", scope="session")
def error_incorrect_api_key_response_fixture() -> str:
    """Define a fixture for error response data (incorrect API key).

    Returns:
        An API response payload.
    """
    return load_fixture("error_incorrect_api_key_response.json")


@pytest.fixture(name="error_key_expired_response", scope="session")
def error_key_expired_response_fixture() -> str:
    """Define a fixture for error response data (API key expired).

    Returns:
        An API response payload.
    """
    return load_fixture("error_key_expired_response.json")


@pytest.fixture(name="error_limit_reached_response", scope="session")
def error_limit_reached_response_fixture() -> str:
    """Define a fixture for error response data (API limit reached).

    Returns:
        An API response payload.
    """
    return load_fixture("error_limit_reached_response.json")


@pytest.fixture(name="error_no_nearest_station_response", scope="session")
def error_no_nearest_station_response_fixture() -> str:
    """Define a fixture for error response data (no nearest station).

    Returns:
        An API response payload.
    """
    return load_fixture("error_no_nearest_station_response.json")


@pytest.fixture(name="error_node_not_found_response", scope="session")
def error_node_not_found_response_fixture() -> str:
    """Define a fixture for error response data (Node/Pro not found).

    Returns:
        An API response payload.
    """
    return '"node not found"'


@pytest.fixture(name="error_payment_required_response", scope="session")
def error_payment_required_response_fixture() -> str:
    """Define a fixture for error response data (payment required).

    Returns:
        An API response payload.
    """
    return load_fixture("error_payment_required_response.json")


@pytest.fixture(name="error_permission_denied_response", scope="session")
def error_permission_denied_response_fixture() -> str:
    """Define a fixture for error response data (permission denied to API key).

    Returns:
        An API response payload.
    """
    return load_fixture("error_permission_denied_response.json")


@pytest.fixture(name="node_by_id_response", scope="session")
def node_by_id_response_fixture() -> str:
    """Define a fixture for response data containing a single Node/Pro unit.

    Returns:
        An API response payload.
    """
    return load_fixture("node_by_id_response.json")


@pytest.fixture(name="states_response", scope="session")
def states_response_fixture() -> str:
    """Define a fixture for response data containing a list of states.

    Returns:
        An API response payload.
    """
    return load_fixture("states_response.json")


@pytest.fixture(name="station_response", scope="session")
def station_response_fixture() -> str:
    """Define a fixture for response data containing a single station.

    Returns:
        An API response payload.
    """
    return load_fixture("station_response.json")


@pytest.fixture(name="stations_response", scope="session")
def stations_response_fixture() -> str:
    """Define a fixture for response data containing a list of stations.

    Returns:
        An API response payload.
    """
    return load_fixture("stations_response.json")
