"""Define an object to interact with an AirVisual Node/Pro."""
import asyncio
import json
import logging
import tempfile
from typing import Awaitable, Callable

from smb.SMBConnection import SMBConnection

from .errors import NodeProError

NODE_URL_SCAFFOLD = "https://www.airvisual.com/api/v2/node"

_LOGGER = logging.getLogger(__name__)


class Node:
    """Define the "API" object."""

    def __init__(self, request: Callable[..., Awaitable[dict]]) -> None:
        """Iniitialize."""
        self._request: Callable[..., Awaitable[dict]] = request

    async def from_cloud_api(self, node_id: str) -> dict:
        """Return cloud API data from a node its ID."""
        return await self._request("get", node_id, base_url=NODE_URL_SCAFFOLD)

    async def from_samba(self, ip_or_hostname: str, password: str) -> dict:
        """Return local data from a node (via Samba)."""
        loop = asyncio.get_event_loop()
        conn = SMBConnection("airvisual", password, "whatever", "airvisual")
        tmp_file = tempfile.NamedTemporaryFile()

        def load_latest_measurements():
            """Connect to the AirVisual Node/Pro via Samba."""
            try:
                conn.connect(ip_or_hostname)
                conn.retrieveFile(
                    "airvisual", "/latest_config_measurements.json", tmp_file
                )
                conn.close()
            except Exception as err:  # pylint: disable=broad-except
                raise NodeProError(f"Error while connecting to unit: {err}") from None

        await loop.run_in_executor(None, load_latest_measurements)

        tmp_file.seek(0)
        raw = tmp_file.read()
        tmp_file.close()

        return json.loads(raw.decode())
