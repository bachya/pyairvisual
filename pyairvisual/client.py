"""Define a client to interact with AirVisual."""
from aiohttp import ClientSession, client_exceptions

from .data import Data
from .errors import RequestError, raise_error
from .supported import Supported

API_URL_SCAFFOLD = 'https://api.airvisual.com/v2'


class Client(object):
    """Define the client."""

    def __init__(self, api_key: str, websession: ClientSession) -> None:
        """Initialize."""
        self._api_key = api_key
        self.websession = websession

        self.data = Data(self.request)
        self.supported = Supported(self.request)

    async def request(
            self,
            method: str,
            endpoint: str,
            *,
            headers: dict = None,
            params: dict = None,
            json: dict = None) -> dict:
        """Make a request against AirVisual."""
        if not headers:
            headers = {}
        headers.update({'Content-Type': 'application/json'})

        if not params:
            params = {}
        params.update({'key': self._api_key})

        try:
            async with self.websession.request(
                    method, '{0}/{1}'.format(API_URL_SCAFFOLD, endpoint),
                    headers=headers, params=params, json=json) as resp:
                data = await resp.json()
                _raise_on_error(data)
                return data
        except client_exceptions.ClientError as err:
            raise RequestError('An error occurred: {0}'.format(err)) from None


def _raise_on_error(data: dict) -> None:
    """Raise the appropriate exception on error."""
    if data['status'] == 'success':
        return

    raise_error(data['data']['message'])
