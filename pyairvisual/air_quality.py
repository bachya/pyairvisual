"""Define an object to retrieve air quality info."""
from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any, cast


class AirQuality:
    """Define an object to manage air quality API calls."""

    def __init__(self, request: Callable[..., Awaitable]) -> None:
        """Initialize.

        Args:
            request: The request method from the CloudAPI object.
        """
        self._request = request

    async def _nearest(
        self,
        kind: str,
        latitude: float | str | None = None,
        longitude: float | str | None = None,
    ) -> dict[str, Any]:
        """Return data from nearest city/station (IP or coordinates).

        Args:
            kind: "city" or "station".
            latitude: A latitude.
            longitude: A longitude.

        Returns:
            An API response payload.
        """
        if latitude and longitude:
            params = {"lat": str(latitude), "lon": str(longitude)}
        else:
            params = {}

        data = await self._request("get", f"nearest_{kind}", params=params)
        return cast(dict[str, Any], data["data"])

    async def city(self, city: str, state: str, country: str) -> dict[str, Any]:
        """Return data for the specified city.

        Args:
            city: A city.
            state: A state.
            country: A country.

        Returns:
            An API response payload.
        """
        data = await self._request(
            "get", "city", params={"city": city, "state": state, "country": country}
        )
        return cast(dict[str, Any], data["data"])

    async def nearest_city(
        self,
        latitude: float | str | None = None,
        longitude: float | str | None = None,
    ) -> dict[str, Any]:
        """Return data from nearest city (IP or coordinates).

        Args:
            latitude: A latitude.
            longitude: A longitude.

        Returns:
            An API response payload.
        """
        return await self._nearest("city", latitude, longitude)

    async def nearest_station(
        self,
        latitude: float | str | None = None,
        longitude: float | str | None = None,
    ) -> dict[str, Any]:
        """Return data from nearest station (IP or coordinates).

        Args:
            latitude: A latitude.
            longitude: A longitude.

        Returns:
            An API response payload.
        """
        return await self._nearest("station", latitude, longitude)

    async def ranking(self) -> list[dict[str, Any]]:
        """Return a sorted array of selected major cities in the world.

        Returns:
            An API response payload.
        """
        data = await self._request("get", "city_ranking")
        return cast(list[dict[str, Any]], data["data"])

    async def station(
        self, station: str, city: str, state: str, country: str
    ) -> dict[str, Any]:
        """Return data for the specified station.

        Args:
            station: A station name.
            city: A city.
            state: A state.
            country: A country.

        Returns:
            An API response payload.
        """
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
        return cast(dict[str, Any], data["data"])
