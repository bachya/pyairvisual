"""Run an example script to quickly test."""
import asyncio
import logging

from aiohttp import ClientSession

from pyairvisual import Client
from pyairvisual.errors import AirVisualError, UnauthorizedError

_LOGGER = logging.getLogger(__name__)

API_KEY = "<API_KEY>"


async def main() -> None:  # pylint: disable=too-many-statements
    """Create the aiohttp session and run the example."""
    logging.basicConfig(level=logging.INFO)
    async with ClientSession() as websession:
        client = Client(websession, api_key=API_KEY)

        # Get supported locations (by location):
        try:
            _LOGGER.info(await client.supported.countries())
            _LOGGER.info(await client.supported.states("USA"))
            _LOGGER.info(await client.supported.cities("USA", "Colorado"))
        except AirVisualError as err:
            _LOGGER.error("There was an error: %s", err)

        # Get supported locations (by station):
        try:
            _LOGGER.info(await client.supported.stations("USA", "Colorado", "Denver"))
        except UnauthorizedError as err:
            _LOGGER.error(err)
        except AirVisualError as err:
            _LOGGER.error("There was an error: %s", err)

        # Get data by nearest location (by IP):
        try:
            _LOGGER.info(await client.api.nearest_city())
        except AirVisualError as err:
            _LOGGER.error("There was an error: %s", err)

        # Get data by nearest location (coordinates or explicit location):
        try:
            _LOGGER.info(
                await client.api.nearest_city(
                    latitude=39.742599, longitude=-104.9942557
                )
            )
            _LOGGER.info(
                await client.api.city(
                    city="Los Angeles", state="California", country="USA"
                )
            )
        except AirVisualError as err:
            _LOGGER.error("There was an error: %s", err)

        # Get data by nearest station (by IP):
        try:
            _LOGGER.info(await client.api.nearest_station())
        except UnauthorizedError as err:
            _LOGGER.error(err)
        except AirVisualError as err:
            _LOGGER.error("There was an error: %s", err)

        # Get data by nearest station (by coordinates or explicit location):
        try:
            _LOGGER.info(
                await client.api.nearest_station(
                    latitude=39.742599, longitude=-104.9942557
                )
            )
            _LOGGER.info(
                await client.api.station(
                    station="US Embassy in Beijing",
                    city="Beijing",
                    state="Beijing",
                    country="China",
                )
            )
        except UnauthorizedError as err:
            _LOGGER.error(err)
        except AirVisualError as err:
            _LOGGER.error("There was an error: %s", err)

        # Get data on AQI ranking:
        try:
            _LOGGER.info(await client.api.ranking())
        except UnauthorizedError as err:
            _LOGGER.error(err)
        except AirVisualError as err:
            _LOGGER.error("There was an error: %s", err)

        # Get info on a AirVisual Pro node:
        _LOGGER.info(await client.api.node("zEp8CifbnasWtToBc"))


asyncio.get_event_loop().run_until_complete(main())
