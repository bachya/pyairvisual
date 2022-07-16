"""Define an object to retrieve air quality info."""
from __future__ import annotations

from typing import Any, Awaitable, Callable


class AirQuality:
    """Define an object to manage air quality API calls."""

    def __init__(self, request: Callable[..., Awaitable]) -> None:
        """Iniitialize."""
        self._request = request

    async def _nearest(
        self,
        kind: str,
        latitude: float | str | None = None,
        longitude: float | str | None = None,
    ) -> dict[str, Any]:
        """Return data from nearest city/station (IP or coordinates)."""
        if latitude and longitude:
            params = {"lat": str(latitude), "lon": str(longitude)}
        else:
            params = {}

        data = await self._request("get", f"nearest_{kind}", params=params)
        return data["data"]

    async def city(self, city: str, state: str, country: str) -> dict[str, Any]:
        """Return data for the specified city."""
        data = await self._request(
            "get", "city", params={"city": city, "state": state, "country": country}
        )
        return data["data"]

    async def nearest_city(
        self,
        latitude: float | str | None = None,
        longitude: float | str | None = None,
    ) -> dict[str, Any]:
        """Return data from nearest city (IP or coordinates)."""
        return await self._nearest("city", latitude, longitude)

    async def nearest_station(
        self,
        latitude: float | str | None = None,
        longitude: float | str | None = None,
    ) -> dict[str, Any]:
        """Return data from nearest station (IP or coordinates)."""
        return await self._nearest("station", latitude, longitude)

    async def ranking(self) -> dict[str, Any]:
        """Return a sorted array of selected major cities in the world."""
        data = await self._request("get", "city_ranking")
        return data["data"]

    async def station(
        self, station: str, city: str, state: str, country: str
    ) -> dict[str, Any]:
        """Return data for the specified station."""
        data = await self._request(
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
