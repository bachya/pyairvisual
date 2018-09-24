"""Define a series of endpoints for what locations are supported."""
from typing import Awaitable, Callable


class Supported:
    """Define the "Supported" endpoint group."""

    def __init__(self, request: Callable[..., Awaitable[dict]]) -> None:
        """Iniitialize."""
        self._request = request

    async def cities(self, country: str, state: str) -> list:
        """Return a list of supported cities in a country/state."""
        data = await self._request(
            'get', 'cities', params={
                'state': state,
                'country': country
            })
        return [d['city'] for d in data['data']]

    async def countries(self) -> list:
        """Return an array of all supported countries."""
        data = await self._request('get', 'countries')
        return [d['country'] for d in data['data']]

    async def states(self, country: str) -> list:
        """Return a list of supported states in a country."""
        data = await self._request(
            'get', 'states', params={'country': country})
        return [d['state'] for d in data['data']]

    async def stations(self, city: str, state: str, country: str) -> list:
        """Return a list of supported stations in a city."""
        data = await self._request(
            'get',
            'stations',
            params={
                'city': city,
                'state': state,
                'country': country
            })
        return [station for station in data['data']]
