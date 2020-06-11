"""Define a series of endpoints for what locations are supported."""
from typing import Callable, Coroutine


class Supported:
    """Define an object to supported location API calls."""

    def __init__(self, request: Callable[..., Coroutine]) -> None:
        """Iniitialize."""
        self._request: Callable[..., Coroutine] = request

    async def cities(self, country: str, state: str) -> list:
        """Return a list of supported cities in a country/state."""
        data: dict = await self._request(
            "get", "cities", params={"state": state, "country": country}
        )
        return [d["city"] for d in data["data"]]

    async def countries(self) -> list:
        """Return an array of all supported countries."""
        data: dict = await self._request("get", "countries")
        return [d["country"] for d in data["data"]]

    async def states(self, country: str) -> list:
        """Return a list of supported states in a country."""
        data: dict = await self._request("get", "states", params={"country": country})
        return [d["state"] for d in data["data"]]

    async def stations(self, city: str, state: str, country: str) -> list:
        """Return a list of supported stations in a city."""
        data: dict = await self._request(
            "get", "stations", params={"city": city, "state": state, "country": country}
        )
        return data["data"]
