"""Define a client to interact with AirVisual."""
from json.decoder import JSONDecodeError
from typing import Optional

import aiohttp

from .api import API, API_URL_SCAFFOLD
from .errors import raise_error
from .node import Node
from .supported import Supported


class Client:  # pylint: disable=too-few-public-methods
    """Define the client."""

    def __init__(
        self, websession: aiohttp.ClientSession, *, api_key: Optional[str] = None
    ) -> None:
        """Initialize."""
        self._api_key: Optional[str] = api_key
        self.websession: aiohttp.ClientSession = websession

        self.api: API = API(self.request)
        self.node: Node = Node(self.request)
        self.supported: Supported = Supported(self.request)

    async def request(
        self,
        method: str,
        endpoint: str,
        *,
        base_url: str = API_URL_SCAFFOLD,
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        json: Optional[dict] = None,
    ) -> dict:
        """Make a request against AirVisual."""
        if not headers:
            headers = {}
        headers.update({"Content-Type": "application/json"})

        if not params:
            params = {}

        if self._api_key:
            params.update({"key": self._api_key})

        async with self.websession.request(
            method, f"{base_url}/{endpoint}", headers=headers, params=params, json=json
        ) as resp:
            try:
                data = await resp.json(content_type=None)
            except JSONDecodeError:
                # The response can't be parsed as JSON, so we'll use its body text
                # in an error:
                response_text = await resp.text()
                data = {"status": "fail", "data": {"message": response_text}}

            if isinstance(data, str):
                # In some cases, the AirVisual API will return a quoted string in its
                # response body (e.g., "\"node not found\""), which is technically valid
                # JSON. Additionally, AirVisual sets that response's Content-Type header
                # to application/json (#smh). Together, these facotrs will allow a
                # non-true-JSON  payload to escape the try/except above. So, if we get
                # here, we use the string value (with quotes removed) to raise an error:
                response_text = data.replace('"', "")
                data = {"status": "fail", "data": {"message": response_text}}

            _raise_on_error(data)
            return data


def _raise_on_error(data: dict) -> None:
    """Raise the appropriate exception on error."""
    if "status" in data and data["status"] != "success":
        raise_error(data["data"]["message"])
