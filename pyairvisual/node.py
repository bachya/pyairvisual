"""Define objects to interact with an AirVisual Node/Pro."""
# pylint: disable=too-few-public-methods
import asyncio
from collections import OrderedDict
import csv
import json
import logging
import tempfile
from types import TracebackType
from typing import Callable, Coroutine, List, Optional, Set, Type

import numpy as np
import smb
from smb.SMBConnection import SMBConnection

from .errors import NodeProError

API_URL_BASE = "https://www.airvisual.com/api/v2/node"

SAMBA_HISTORY_PATTERN = "*_AirVisual_values.txt"
SMB_SERVICE = "airvisual"
SMB_USERNAME = "airvisual"

_LOGGER = logging.getLogger(__name__)

METRIC_AQI_CN = "aqi_cn"
METRIC_AQI_US = "aqi_us"
METRIC_CO2 = "co2"
METRIC_HUMIDITY = "humidity"
METRIC_PM01 = "pm0_1"
METRIC_PM10 = "pm1_0"
METRIC_PM25 = "pm2_5"
METRIC_VOC = "voc"
METRICS_TO_TREND = [
    METRIC_AQI_CN,
    METRIC_AQI_US,
    METRIC_CO2,
    METRIC_HUMIDITY,
    METRIC_PM01,
    METRIC_PM10,
    METRIC_PM25,
    METRIC_VOC,
]

METRIC_MAPPING = {
    "AQI(CN)": METRIC_AQI_CN,
    "AQI(US)": METRIC_AQI_US,
    "CO2(ppm)": METRIC_CO2,
    "Humidity(%RH)": METRIC_HUMIDITY,
    "PM01(ug/m3)": METRIC_PM01,
    "PM10(ug/m3)": METRIC_PM10,
    "PM2_5(ug/m3)": METRIC_PM25,
    "VOC(ppb)": METRIC_VOC,
    "co2_ppm": METRIC_CO2,
    "humidity_RH": METRIC_HUMIDITY,
    "pm01_ugm3": METRIC_PM01,
    "pm10_ugm3": METRIC_PM10,
    "pm25": METRIC_PM25,
    "pm25_AQICN": METRIC_AQI_CN,
    "pm25_AQIUS": METRIC_AQI_US,
    "pm25_ugm3": METRIC_PM25,
    "voc_ppb": METRIC_VOC,
}

TREND_FLAT = "flat"
TREND_INCREASING = "increasing"
TREND_DECREASING = "decreasing"


def _calculate_trends(history: List[OrderedDict], measurements_to_use: int) -> dict:
    """Calculate the trends of all data points in history data."""
    if measurements_to_use == -1:
        index_range = np.arange(0, len(history))
    else:
        index_range = np.arange(0, measurements_to_use)

    measured_attributes: Set = set().union(*(d.keys() for d in history))
    metrics_to_trend = measured_attributes.intersection(list(METRICS_TO_TREND))

    trends = {}
    for attribute in metrics_to_trend:
        values = [
            float(value)
            for measurement in history
            for attr, value in measurement.items()
            if attr == attribute
        ]

        if measurements_to_use != -1:
            values = values[-measurements_to_use:]

        index_array = np.array(values)
        linear_fit = np.polyfit(index_range, index_array, 1,)
        slope = round(linear_fit[0], 2)

        metric = _get_normalized_metric_name(attribute)

        if slope > 0:
            trends[metric] = TREND_INCREASING
        elif slope < 0:
            trends[metric] = TREND_DECREASING
        else:
            trends[metric] = TREND_FLAT

    return trends


def _get_normalized_metric_name(key: str) -> str:
    """Return a normalized string (if it exists) for a metric."""
    return METRIC_MAPPING.get(key, key)


class NodeCloudAPI:
    """Define an object to work with getting Node info via the Cloud API."""

    def __init__(self, request: Callable[..., Coroutine]) -> None:
        """Initialize."""
        self._request: Callable[..., Coroutine] = request

    async def get_by_node_id(self, node_id: str) -> dict:
        """Return cloud API data from a node its ID."""
        return await self._request("get", node_id, base_url=API_URL_BASE)


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
        except ConnectionRefusedError:
            raise NodeProError(
                f"Couldn't find a Node/Pro unit at IP address: {self._ip_or_hostname}"
            )

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

        data = json.loads(raw.decode())

        _LOGGER.debug("Node Pro measurements loaded: %s", data)

        try:
            # Handle a single measurement returned in a list:
            measurements = data["measurements"][0].items()
        except KeyError:
            # Handle a single measurement returned as a standalone dict:
            measurements = data["measurements"].items()

        data["measurements"] = {
            _get_normalized_metric_name(pollutant): value
            for pollutant, value in measurements
        }

        data["status"]["sensor_life"] = {
            _get_normalized_metric_name(pollutant): value
            for pollutant, value in data["status"].get("sensor_life", {}).items()
        }

        return data

    async def async_get_history(
        self, *, include_trends: bool = True, measurements_to_use: int = -1
    ) -> dict:
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
        await self._async_get_file(f"/{history_files[-1].filename}", tmp_file)

        def load_history():
            """Load."""
            data = []
            with open(tmp_file.name) as file:
                reader = csv.DictReader(file, delimiter=";")
                for row in reader:
                    data.append(
                        {
                            _get_normalized_metric_name(header): value
                            for header, value in row.items()
                        }
                    )

            _LOGGER.debug("Node Pro history loaded: %s", data)

            return data

        data = {}

        data["measurements"] = await self._loop.run_in_executor(None, load_history)
        if include_trends:
            data["trends"] = _calculate_trends(
                data["measurements"], measurements_to_use
            )

        return data
