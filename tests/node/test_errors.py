"""Define tests for Node errors."""

# pylint: disable=unused-argument
from collections.abc import Generator
from unittest.mock import Mock

import pytest
import smb

from pyairvisual.node import (
    InvalidAuthenticationError,
    NodeConnectionError,
    NodeProError,
    NodeSamba,
)
from tests.common import TEST_NODE_IP_ADDRESS, TEST_NODE_PASSWORD


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "mock_pysmb_connect,exc,error_str",
    [
        (
            Mock(side_effect=smb.base.NotReadyError),
            InvalidAuthenticationError,
            "The Pro unit returned an authentication error",
        ),
        (
            Mock(side_effect=smb.base.SMBTimeout),
            NodeConnectionError,
            "Timed out while talking to the Pro unit",
        ),
        (
            Mock(side_effect=ConnectionRefusedError),
            NodeConnectionError,
            "Couldn't find a Pro unit at the provided IP address",
        ),
    ],
)
async def test_connect_errors(
    error_str: str,
    exc: type[NodeProError],
    setup_samba_connection: Generator,  # noqa: F841
) -> None:
    """Test various errors arising during connection.

    Args:
        error_str: The logged error message.
        exc: A raised exception (based on NodeProError).
        setup_samba_connection: A mocked Samba connection.
    """
    node = NodeSamba(TEST_NODE_IP_ADDRESS, TEST_NODE_PASSWORD)
    with pytest.raises(exc) as err:
        await node.async_connect()
    assert error_str in str(err)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "mock_pysmb_retrieve_file",
    [
        Mock(side_effect=smb.base.NotConnectedError),
        Mock(side_effect=smb.base.SMBTimeout),
        Mock(side_effect=smb.smb_structs.UnsupportedFeature),
        Mock(side_effect=smb.smb_structs.ProtocolError),
    ],
)
async def test_history_errors(setup_samba_connection: Generator) -> None:  # noqa: F841
    """Test various errors arising while getting history.

    Args:
        setup_samba_connection: A mocked Samba connection.
    """
    node = NodeSamba(TEST_NODE_IP_ADDRESS, TEST_NODE_PASSWORD)
    with pytest.raises(NodeProError):
        await node.async_connect()
        _ = await node.async_get_history()


@pytest.mark.asyncio
@pytest.mark.parametrize("mock_pysmb_connect", [Mock(return_value=False)])
async def test_failed_authentication(
    setup_samba_connection: Generator,  # noqa: F841
) -> None:
    """Test that failed authentication is caught.

    Args:
        setup_samba_connection: A mocked Samba connection.
    """
    node = NodeSamba(TEST_NODE_IP_ADDRESS, TEST_NODE_PASSWORD)
    with pytest.raises(InvalidAuthenticationError):
        await node.async_connect()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "mock_pysmb_retrieve_file",
    [
        Mock(side_effect=smb.base.NotConnectedError),
        Mock(side_effect=smb.base.SMBTimeout),
        Mock(side_effect=smb.smb_structs.UnsupportedFeature),
        Mock(side_effect=smb.smb_structs.ProtocolError),
    ],
)
async def test_measurement_errors(
    setup_samba_connection: Generator,  # noqa: F841
) -> None:
    """Test various errors arising while getting a file via Samba.

    Args:
        setup_samba_connection: A mocked Samba connection.
    """
    node = NodeSamba(TEST_NODE_IP_ADDRESS, TEST_NODE_PASSWORD)
    with pytest.raises(NodeProError):
        await node.async_connect()
        _ = await node.async_get_latest_measurements()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "mock_history_file,mock_pysmb_list_path,node_measurements_file",
    [
        (
            Mock(),
            Mock(return_value=[]),
            "node_measurements_samba_list_response.json",
        )
    ],
)
async def test_node_by_samba_no_history_files(
    setup_samba_connection: Generator,  # noqa: F841
) -> None:
    """Test the Node/Pro not having any history files where expected.

    Args:
        setup_samba_connection: A mocked Samba connection.
    """
    with pytest.raises(NodeProError):
        async with NodeSamba(TEST_NODE_IP_ADDRESS, TEST_NODE_PASSWORD) as node:
            await node.async_get_history()
