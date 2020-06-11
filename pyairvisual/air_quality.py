"""Define an object to retrieve air quality info."""
from typing import Callable, Coroutine, Optional, Union


class AirQuality:
    """Define an object to manage air quality API calls."""

    def __init__(self, request: Callable[..., Coroutine]) -> None:
        """Iniitialize."""
        self._request: Callable[..., Coroutine] = request

    async def _nearest(
        self,
        kind: str,
        latitude: Optional[Union[float, str]] = None,
        longitude: Optional[Union[float, str]] = None,
    ) -> dict:
        """Return data from nearest city/station (IP or coordinates)."""
        params: dict = {}
        if latitude and longitude:
            params.update({"lat": str(latitude), "lon": str(longitude)})

        data: dict = await self._request("get", f"nearest_{kind}", params=params)
        return data["data"]

    async def city(self, city: str, state: str, country: str) -> dict:
        """Return data for the specified city."""
        data: dict = await self._request(
            "get", "city", params={"city": city, "state": state, "country": country}
        )
        return data["data"]

    async def nearest_city(
        self,
        latitude: Optional[Union[float, str]] = None,
        longitude: Optional[Union[float, str]] = None,
    ) -> dict:
        """Return data from nearest city (IP or coordinates)."""
        return await self._nearest("city", latitude, longitude)

    async def nearest_station(
        self,
        latitude: Optional[Union[float, str]] = None,
        longitude: Optional[Union[float, str]] = None,
    ) -> dict:
        """Return data from nearest station (IP or coordinates)."""
        return await self._nearest("station", latitude, longitude)

    async def ranking(self) -> dict:
        """Return a sorted array of selected major cities in the world."""
        data = await self._request("get", "city_ranking")
        return data["data"]

    async def station(self, station: str, city: str, state: str, country: str) -> dict:
        """Return data for the specified station."""
        data: dict = await self._request(
            "get",
            "station",
            params={
                "station": station,
                "city": city,
                "state": state,
                "country": country,
            },
        )
        return data["data"]
