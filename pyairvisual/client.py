"""Define a client to interact with AirVisual."""
from typing import Union

import aiohttp

from .api import API
from .const import API_URL_SCAFFOLD
from .errors import raise_error
from .supported import Supported


class Client:  # pylint: disable=too-few-public-methods
    """Define the client."""

    def __init__(
            self, websession: aiohttp.ClientSession, *,
            api_key: str = None) -> None:
        """Initialize."""
        self._api_key = api_key
        self.websession = websession

        self.api = API(self.request)
        self.supported = Supported(self.request)

    async def request(
            self,
            method: str,
            endpoint: str,
            *,
            base_url: str = API_URL_SCAFFOLD,
            headers: dict = None,
            params: dict = None,
            json: dict = None) -> dict:
        """Make a request against AirVisual."""
        if not headers:
            headers = {}
        headers.update({'Content-Type': 'application/json'})

        if not params:
            params = {}

        if self._api_key:
            params.update({'key': self._api_key})

        url = '{0}/{1}'.format(base_url, endpoint)
        async with self.websession.request(method, url, headers=headers,
                                           params=params, json=json) as resp:
            data = await resp.json(content_type=None)
            _raise_on_error(data)
            return data


def _raise_on_error(data: Union[str, dict]) -> None:
    """Raise the appropriate exception on error."""
    if isinstance(data, str):
        raise_error(data)
    elif 'status' in data and data['status'] != 'success':
        raise_error(data['data']['message'])
