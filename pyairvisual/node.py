"""Define an object to interact with an AirVisual Node/Pro."""
# pylint: disable=too-few-public-methods
import asyncio
from collections import OrderedDict
import csv
import json
import logging
import tempfile
from types import TracebackType
from typing import Awaitable, Callable, List, Optional, Type

import numpy as np
import smb
from smb.SMBConnection import SMBConnection

from .errors import NodeProError

NODE_URL_SCAFFOLD = "https://www.airvisual.com/api/v2/node"

SAMBA_HISTORY_PATTERN = "*_AirVisual_values.txt"
SMB_SERVICE = "airvisual"
SMB_USERNAME = "airvisual"

_LOGGER = logging.getLogger(__name__)

ATTRIBUTES_TO_TREND = [
    "AQI(CN)",
    "AQI(US)",
    "CO2(ppm)",
    "Humidity(%RH)",
    "PM01(ug/m3)",
    "PM10(ug/m3)",
    "PM2_5(ug/m3)",
    "VOC(ppb)",
]

TREND_FLAT = "flat"
TREND_INCREASING = "increasing"
TREND_DECREASING = "decreasing"


def _calculate_trends(history: List[OrderedDict]) -> dict:
    """Calculate the trends of all data points in history data."""
    trends = {}

    for attribute in ATTRIBUTES_TO_TREND:
        _LOGGER.info("Looking at %s", attribute)
        values = [
            float(value)
            for measurement in history
            for attr, value in measurement.items()
            if attr == attribute
        ]

        index_range = np.arange(0, len(values))
        index_array = np.array(values)
        linear_fit = np.polyfit(index_range, index_array, 1,)
        slope = round(linear_fit[0], 2)

        if slope > 0:
            trends[attribute] = TREND_INCREASING
        elif slope < 0:
            trends[attribute] = TREND_DECREASING
        else:
            trends[attribute] = TREND_FLAT

    return trends


class NodeCloudAPI:
    """Define an object to work with getting Node info via the cloud API."""

    def __init__(self, request: Callable[..., Awaitable[dict]]) -> None:
        """Initialize."""
        self._request: Callable[..., Awaitable[dict]] = request

    async def async_get_by_node_id(self, node_id: str) -> dict:
        """Return cloud API data from a node its ID."""
        return await self._request("get", node_id, base_url=NODE_URL_SCAFFOLD)


class NodeSamba:
    """Define an object to work with getting Node info over Samba."""

    def __init__(self, ip_or_hostname: str, password: str) -> None:
        """Initialize."""
        self._conn = SMBConnection(SMB_USERNAME, password, "pyairvisual", SMB_SERVICE)
        self._ip_or_hostname = ip_or_hostname
        self._latest_history = None
        self._loop = asyncio.get_event_loop()

    async def __aenter__(self) -> "NodeSamba":
        """Handle the start of a context manager."""
        await self.async_connect()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Handle the end of a context manager."""
        await self.async_disconnect()

    async def _async_get_file(
        self, filepath: str, file_obj: tempfile.NamedTemporaryFile,  # type: ignore
    ) -> None:
        """Save a file to a tempfile object."""

        def get():
            """Get the file."""
            self._conn.retrieveFile(SMB_SERVICE, filepath, file_obj)

        try:
            await self._loop.run_in_executor(None, get)
        except smb.base.NotConnectedError as err:
            raise NodeProError(f"The connection to the Node/Pro unit broke: {err}")
        except smb.base.SMBTimeout:
            raise NodeProError("Timed out retrieving {filepath}")
        except Exception as err:  # pylint: disable=broad-except
            raise NodeProError(f"Error while retrieving {filepath}: {err}")

    async def async_connect(self) -> None:
        """Return cloud API data from a node its ID."""

        def connect():
            """Connect."""
            self._conn.connect(self._ip_or_hostname)

        try:
            await self._loop.run_in_executor(None, connect)
        except smb.base.NotReadyError as err:
            raise NodeProError(f"The Node/Pro unit can't be connected to: {err}")
        except smb.base.SMBTimeout:
            raise NodeProError("Timed out while connecting to the Node/Pro unit")

    async def async_disconnect(self) -> None:
        """Return cloud API data from a node its ID."""

        def disconnect():
            """Connect."""
            self._conn.close()

        await self._loop.run_in_executor(None, disconnect)

    async def async_get_latest_measurements(self) -> dict:
        """Get the latest measurements from the device."""
        tmp_file = tempfile.NamedTemporaryFile()
        await self._async_get_file("/latest_config_measurements.json", tmp_file)
        tmp_file.seek(0)
        raw = tmp_file.read()
        tmp_file.close()
        return json.loads(raw.decode())

    async def async_get_history(self) -> List[OrderedDict]:
        """Get history data from the device."""

        def search_history():
            """Search for the most recent history file."""
            try:
                return self._conn.listPath(
                    SMB_SERVICE,
                    "/",
                    search=smb.smb_constants.SMB_FILE_ATTRIBUTE_NORMAL,
                    pattern=SAMBA_HISTORY_PATTERN,
                )
            except smb.base.NotConnectedError as err:
                raise NodeProError(f"The connection to the Node/Pro unit broke: {err}")
            except smb.base.SMBTimeout:
                raise NodeProError("Timed out retrieving current history data")
            except Exception as err:  # pylint: disable=broad-except
                raise NodeProError(f"Error while retrieving history data: {err}")

        history_files = await self._loop.run_in_executor(None, search_history)

        if not history_files:
            raise NodeProError(
                f"No history files found that match {SAMBA_HISTORY_PATTERN}"
            )

        tmp_file = tempfile.NamedTemporaryFile()
        await self._async_get_file(f"/{history_files[0].filename}", tmp_file)

        def load_history():
            """Load."""
            with open(tmp_file.name) as file:
                return list(csv.DictReader(file, delimiter=";"))

        history = await self._loop.run_in_executor(None, load_history)

        return history


class Node:
    """Define the "Node" object."""

    def __init__(self, request: Callable[..., Awaitable[dict]]) -> None:
        """Initialize."""
        self._cloud_api = NodeCloudAPI(request)

    async def from_cloud_api(self, node_id: str) -> dict:
        """Return cloud API data from a node its ID."""
        return await self._cloud_api.async_get_by_node_id(node_id)

    async def from_samba(
        self,
        ip_or_hostname: str,
        password: str,
        include_history: bool = True,
        include_trends: bool = True,
    ) -> dict:
        """Return local data from a node (via Samba)."""
        data = {}

        async with NodeSamba(ip_or_hostname, password) as node:
            data["current"] = await node.async_get_latest_measurements()

            if not include_history and not include_trends:
                return data

            history = await node.async_get_history()
            if include_history:
                data["history"] = history  # type: ignore
            if include_trends:
                data["trends"] = _calculate_trends(history)

        return data
