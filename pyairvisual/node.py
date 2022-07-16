"""Define objects to interact with an AirVisual Node/Pro."""
from __future__ import annotations

import asyncio
from collections import OrderedDict
import csv
import json
import tempfile
from types import TracebackType
from typing import Any, Awaitable, Callable

import numpy as np
import smb
from smb.SMBConnection import SMBConnection

from .const import LOGGER
from .errors import NodeProError

API_URL_BASE = "https://www.airvisual.com/api/v2/node"

SAMBA_HISTORY_PATTERN = "*_AirVisual_values.txt"
SMB_SERVICE = "airvisual"
SMB_USERNAME = "airvisual"

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


def _calculate_trends(
    history: list[OrderedDict], measurements_to_use: int
) -> dict[str, Any]:
    """Calculate the trends of all data points in history data."""
    if measurements_to_use == -1:
        index_range = np.arange(0, len(history))
    else:
        index_range = np.arange(0, measurements_to_use)

    measured_attributes = set().union(*(d.keys() for d in history))
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
        linear_fit = np.polyfit(
            index_range,
            index_array,
            1,
        )
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


class NodeCloudAPI:  # pylint: disable=too-few-public-methods
    """Define an object to work with getting Node info via the Cloud API."""

    def __init__(self, request: Callable[..., Awaitable]) -> None:
        """Initialize."""
        self._request = request

    async def get_by_node_id(self, node_id: str) -> dict[str, Any]:
        """Return cloud API data from a node its ID."""
        return await self._request("get", node_id, base_url=API_URL_BASE)


class NodeSamba:
    """Define an object to work with getting Node info over Samba."""

    def __init__(self, ip_or_hostname: str, password: str) -> None:
        """Initialize."""
        self._conn = SMBConnection(SMB_USERNAME, password, "pyairvisual", SMB_SERVICE)
        self._connected = False
        self._ip_or_hostname = ip_or_hostname
        self._latest_history = None
        self._loop = asyncio.get_event_loop()

    async def __aenter__(self) -> "NodeSamba":
        """Handle the start of a context manager."""
        await self.async_connect()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Handle the end of a context manager."""
        await self.async_disconnect()

    async def _async_execute_samba_command(self, func: Callable):
        """Execute (and catch errors with) a Samba command."""
        try:
            result = await self._loop.run_in_executor(None, func)
        except smb.base.NotReadyError as err:
            raise NodeProError(f"The Node/Pro unit returned an error: {err}") from None
        except smb.base.SMBTimeout:
            raise NodeProError("Timed out while talking to the Node/Pro unit") from None
        except ConnectionRefusedError:
            raise NodeProError(
                f"Couldn't find a Node/Pro unit at IP address: {self._ip_or_hostname}"
            ) from None
        except Exception as err:  # pylint: disable=broad-except
            raise NodeProError(err) from None

        if result is False:
            raise NodeProError("No data or results returned") from None

        return result

    async def _async_get_file(
        self,
        filepath: str,
        file_obj: tempfile.NamedTemporaryFile,  # type: ignore
    ) -> None:
        """Save a file to a tempfile object."""

        def get():
            """Get the file."""
            return self._conn.retrieveFile(SMB_SERVICE, filepath, file_obj)

        await self._async_execute_samba_command(get)

    async def async_connect(self) -> None:
        """Return cloud API data from a node its ID."""

        def connect():
            """Connect."""
            return self._conn.connect(self._ip_or_hostname)

        await self._async_execute_samba_command(connect)
        self._connected = True

    async def async_disconnect(self) -> None:
        """Return cloud API data from a node its ID."""

        def disconnect():
            """Connect."""
            return self._conn.close()

        if self._connected:
            await self._async_execute_samba_command(disconnect)
            self._connected = False

    async def async_get_latest_measurements(self) -> dict[str, Any]:
        """Get the latest measurements from the device."""
        tmp_file = tempfile.NamedTemporaryFile()
        await self._async_get_file("/latest_config_measurements.json", tmp_file)
        tmp_file.seek(0)
        raw = tmp_file.read()
        tmp_file.close()

        data = json.loads(raw.decode())

        LOGGER.debug("Node Pro measurements loaded: %s", data)

        try:
            # Handle a single measurement returned in a list:
            measurements = data["measurements"][0].items()
        except KeyError:
            # Handle a single measurement returned as a standalone dict:
            measurements = data["measurements"].items()

        data["last_measurement_timestamp"] = int(data["date_and_time"]["timestamp"])

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
    ) -> dict[str, Any]:
        """Get history data from the device."""

        def search_history():
            """Search for the most recent history file."""
            return self._conn.listPath(
                SMB_SERVICE,
                "/",
                search=smb.smb_constants.SMB_FILE_ATTRIBUTE_NORMAL,
                pattern=SAMBA_HISTORY_PATTERN,
            )

        history_files = await self._async_execute_samba_command(search_history)

        if not history_files:
            raise NodeProError(
                f"No history files found that match {SAMBA_HISTORY_PATTERN}"
            )

        tmp_file = tempfile.NamedTemporaryFile()
        await self._async_get_file(f"/{history_files[-1].filename}", tmp_file)

        def load_history():
            """Load."""
            data = []
            with open(tmp_file.name, encoding="utf-8") as file:
                reader = csv.DictReader(file, delimiter=";")
                for row in reader:
                    data.append(
                        {
                            _get_normalized_metric_name(header): value
                            for header, value in row.items()
                        }
                    )

            LOGGER.debug("Node Pro history loaded: %s", data)

            return data

        data = {}

        data["measurements"] = await self._loop.run_in_executor(None, load_history)
        if include_trends:
            data["trends"] = _calculate_trends(
                data["measurements"], measurements_to_use
            )

        return data
