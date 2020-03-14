"""Define an object to interact with an AirVisual Node/Pro."""
import logging
from typing import Awaitable, Callable

NODE_URL_SCAFFOLD = "https://www.airvisual.com/api/v2/node"

_LOGGER = logging.getLogger(__name__)


class Node:  # pylint: disable=too-few-public-methods
    """Define the "API" object."""

    def __init__(self, request: Callable[..., Awaitable[dict]]) -> None:
        """Iniitialize."""
        self._request: Callable[..., Awaitable[dict]] = request

    async def from_cloud_api(self, node_id: str) -> dict:
        """Return cloud API data from a node its ID."""
        return await self._request("get", node_id, base_url=NODE_URL_SCAFFOLD)
