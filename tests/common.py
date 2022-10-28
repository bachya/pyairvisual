"""Define common test utilities."""
import os

TEST_API_KEY = "12345"
TEST_CITY = "Los Angeles"
TEST_COUNTRY = "USA"
TEST_LATITUDE = 34.0669
TEST_LONGITUDE = -118.2417
TEST_NODE_ID = "12345"
TEST_NODE_IP_ADDRESS = "192.168.1.100"
TEST_NODE_PASSWORD = "abcde12345"  # noqa: S105
TEST_STATE = "California"
TEST_STATION_NAME = "US Embassy in Beijing"


def load_fixture(filename: str) -> str:
    """Load a fixture.

    Args:
        filename: The filename of the fixtures/ file to load.

    Returns:
        A string containing the contents of the file.
    """
    path = os.path.join(os.path.dirname(__file__), "fixtures", filename)
    with open(path, encoding="utf-8") as fptr:
        return fptr.read()
