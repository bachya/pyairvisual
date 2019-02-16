"""Define an object to interact with the AirVisual data API."""
from typing import Awaitable, Callable, Union

from .const import NODE_URL_SCAFFOLD


class API:
    """Define the "API" object."""

    def __init__(self, request: Callable[..., Awaitable[dict]]) -> None:
        """Iniitialize."""
        self._request = request

    async def _nearest(
            self,
            kind: str,
            latitude: Union[float, str] = None,
            longitude: Union[float, str] = None) -> dict:
        """Return data from nearest city/station (IP or coordinates)."""
        params = {}
        if latitude and longitude:
            params.update({'lat': str(latitude), 'lon': str(longitude)})

        data = await self._request(
            'get', 'nearest_{0}'.format(kind), params=params)
        return data['data']

    async def city(self, city: str, state: str, country: str) -> dict:
        """Return data for the specified city."""
        data = await self._request(
            'get',
            'city',
            params={
                'city': city,
                'state': state,
                'country': country
            })
        return data['data']

    async def nearest_city(
            self,
            latitude: Union[float, str] = None,
            longitude: Union[float, str] = None) -> dict:
        """Return data from nearest city (IP or coordinates)."""
        return await self._nearest('city', latitude, longitude)

    async def nearest_station(
            self,
            latitude: Union[float, str] = None,
            longitude: Union[float, str] = None) -> dict:
        """Return data from nearest station (IP or coordinates)."""
        return await self._nearest('station', latitude, longitude)

    async def node(self, node_id: str) -> dict:
        """Return data from a node by its ID."""
        return await self._request('get', node_id, base_url=NODE_URL_SCAFFOLD)

    async def ranking(self) -> dict:
        """Return a sorted array of selected major cities in the world."""
        data = await self._request('get', 'city_ranking')
        return data['data']

    async def station(
            self, station: str, city: str, state: str, country: str) -> dict:
        """Return data for the specified city."""
        data = await self._request(
            'get',
            'station',
            params={
                'station': station,
                'city': city,
                'state': state,
                'country': country
            })
        return data['data']
