"""Define dynamic test fixtures."""
import tempfile
from unittest.mock import Mock, mock_open, patch

import pytest

from tests.common import load_fixture


@pytest.fixture(name="error_node_not_found_response", scope="session")
def error_node_not_found_response_fixture():
    """Define a fixture for error response data (Node/Pro not found)."""
    return '"node not found"'


@pytest.fixture(name="mock_history_file")
def mock_history_file_fixture():
    """Define a fixture to mock a file for history data."""
    return Mock(name="202003_AirVisual_values.txt")


@pytest.fixture(name="mock_measurements_file")
def mock_measurements_file_fixture(node_measurements_response):
    """Define a fixture to mock a file for measurement data."""
    mock = Mock()
    mock.read.return_value = node_measurements_response.encode()
    return mock


@pytest.fixture(name="mock_open_function", scope="session")
def mock_open_function_fixture(node_history_samba_response):
    """Define a fixture to mock the builtin open function."""
    mop = mock_open(read_data=node_history_samba_response)
    mop.return_value.__iter__ = lambda self: self
    mop.return_value.__next__ = lambda self: next(iter(self.readline, ""))
    return mop


@pytest.fixture(name="mock_pysmb_close")
def mock_pysmb_close_fixture():
    """Define a fixture to mock the pysmb close method."""
    return Mock()


@pytest.fixture(name="mock_pysmb_connect")
def mock_pysmb_connect_fixture():
    """Define a fixture to mock the pysmb connect method."""
    return Mock(return_value=True)


@pytest.fixture(name="mock_pysmb_list_path")
def mock_pysmb_list_path_fixture(mock_history_file):
    """Define a fixture to mock the pysmb listPath method."""
    return Mock(return_value=[mock_history_file])


@pytest.fixture(name="mock_pysmb_retrieve_file")
def mock_pysmb_retrieve_file_fixture():
    """Define a fixture to mock the pysmb retrieveFile method."""
    return Mock()


@pytest.fixture(name="node_history_samba_response", scope="session")
def node_history_samba_response_fixture():
    """Define a fixture for response data containing Node/Pro history info."""
    return load_fixture("node_history_samba_response.txt")


@pytest.fixture(name="node_measurements_file")
def node_measurements_file_fixture():
    """Define a fixture for response data containing Node/Pro measurements."""
    return "node_measurements_samba_dict_response.json"


@pytest.fixture(name="node_measurements_response")
def node_measurements_response_fixture(node_measurements_file):
    """Define a fixture for a fixture filename containing Node/Pro measurements."""
    return load_fixture(node_measurements_file)


@pytest.fixture(name="setup_samba_connection")
def setup_samba_connection_fixture(
    mock_history_file,
    mock_measurements_file,
    mock_open_function,
    mock_pysmb_close,
    mock_pysmb_connect,
    mock_pysmb_list_path,
    mock_pysmb_retrieve_file,
):
    """Define a fixture to return a patched Node/Pro Samba connection."""
    with patch.object(
        tempfile,
        "NamedTemporaryFile",
        side_effect=[mock_measurements_file, mock_history_file],
    ), patch("smb.SMBConnection.SMBConnection.connect", mock_pysmb_connect), patch(
        "smb.SMBConnection.SMBConnection.listPath", mock_pysmb_list_path
    ), patch(
        "smb.SMBConnection.SMBConnection.retrieveFile", mock_pysmb_retrieve_file
    ), patch(
        "smb.SMBConnection.SMBConnection.close", mock_pysmb_close
    ), patch(
        "builtins.open", mock_open_function
    ):
        yield
