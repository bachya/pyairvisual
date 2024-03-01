"""Define dynamic test fixtures."""

from __future__ import annotations

import tempfile
from collections.abc import Generator
from typing import cast
from unittest.mock import MagicMock, Mock, mock_open, patch

import pytest

from tests.common import load_fixture


@pytest.fixture(name="error_node_not_found_response", scope="session")
def error_node_not_found_response_fixture() -> str:
    """Define a fixture for error response data (Node/Pro not found).

    Returns:
        An API response payload.
    """
    return '"node not found"'


@pytest.fixture(name="mock_history_file")
def mock_history_file_fixture() -> Mock:
    """Define a fixture to mock a file for history data.

    Returns:
        A Mock history file.
    """
    return Mock(name="202003_AirVisual_values.txt")


@pytest.fixture(name="mock_measurements_file")
def mock_measurements_file_fixture(node_measurements_response: str) -> Mock:
    """Define a fixture to mock a file for measurement data.

    Returns:
        A Mock measurements file.
    """
    mock = Mock()
    mock.read.return_value = node_measurements_response.encode()
    return mock


@pytest.fixture(name="mock_open_function", scope="session")
def mock_open_function_fixture(node_history_samba_response: str) -> MagicMock:
    """Define a fixture to mock the builtin open function.

    Returns:
        A Mock method to simulate opening a file.
    """
    mop = mock_open(read_data=node_history_samba_response)
    mop.return_value.__iter__ = lambda self: self
    mop.return_value.__next__ = lambda self: next(iter(self.readline, ""))
    return cast(MagicMock, mop)


@pytest.fixture(name="mock_pysmb_close")
def mock_pysmb_close_fixture() -> Mock:
    """Define a fixture to mock the pysmb close method.

    Returns:
        A Mock method to simulate closing the connection to a Node.
    """
    return Mock()


@pytest.fixture(name="mock_pysmb_connect")
def mock_pysmb_connect_fixture() -> Mock:
    """Define a fixture to mock the pysmb connect method.

    Returns:
        A Mock method to simulate opening the connection to a Node.
    """
    return Mock(return_value=True)


@pytest.fixture(name="mock_pysmb_list_path")
def mock_pysmb_list_path_fixture(mock_history_file: Mock) -> Mock:
    """Define a fixture to mock the pysmb listPath method.

    Returns:
        A Mock method to simulate returning the file references at a path.
    """
    return Mock(return_value=[mock_history_file])


@pytest.fixture(name="mock_pysmb_retrieve_file")
def mock_pysmb_retrieve_file_fixture() -> Mock:
    """Define a fixture to mock the pysmb retrieveFile method.

    Returns:
        A Mock method to simulate retrieving the contents of a file.
    """
    return Mock()


@pytest.fixture(name="node_history_samba_response", scope="session")
def node_history_samba_response_fixture() -> str:
    """Define a fixture for response data containing Node/Pro history info.

    Returns:
        An API response payload.
    """
    return load_fixture("node_history_samba_response.txt")


@pytest.fixture(name="node_measurements_file")
def node_measurements_file_fixture() -> str:
    """Define a fixture for response data containing Node/Pro measurements.

    Returns:
        An API response payload.
    """
    return "node_measurements_samba_dict_response.json"


@pytest.fixture(name="node_measurements_response")
def node_measurements_response_fixture(node_measurements_file: Mock) -> str:
    """Define a fixture for a fixture filename containing Node/Pro measurements.

    Returns:
        An API response payload.
    """
    return load_fixture(node_measurements_file)


@pytest.fixture(name="setup_samba_connection")
def setup_samba_connection_fixture(  # pylint: disable=too-many-arguments
    mock_history_file: Mock,
    mock_measurements_file: Mock,
    mock_open_function: Mock,
    mock_pysmb_close: Mock,
    mock_pysmb_connect: Mock,
    mock_pysmb_list_path: Mock,
    mock_pysmb_retrieve_file: Mock,
) -> Generator:
    """Define a fixture to return a patched Node/Pro Samba connection.

    Args:
        mock_history_file: A mocked history file.
        mock_measurements_file: A mocked measurements file.
        mock_open_function: A mocked function to open a file.
        mock_pysmb_close: A mocked function to close a pysmb connection.
        mock_pysmb_connect: A mocked function to open a pysmb connection.
        mock_pysmb_list_path: A mocked function to list file references at a path.
        mock_pysmb_retrieve_file: A mocked function to retrieve the contents of a file.
    """
    with patch.object(
        tempfile,
        "NamedTemporaryFile",
        side_effect=[mock_measurements_file, mock_history_file],
    ), patch("smb.SMBConnection.SMBConnection.connect", mock_pysmb_connect), patch(
        "smb.SMBConnection.SMBConnection.listPath", mock_pysmb_list_path
    ), patch(
        "smb.SMBConnection.SMBConnection.retrieveFile", mock_pysmb_retrieve_file
    ), patch("smb.SMBConnection.SMBConnection.close", mock_pysmb_close), patch(
        "builtins.open", mock_open_function
    ):
        yield
