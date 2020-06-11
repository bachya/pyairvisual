"""Run an example against the AirVisual cloud API."""
import asyncio
import logging

from aiohttp import ClientSession

from pyairvisual import CloudAPI
from pyairvisual.errors import AirVisualError, UnauthorizedError

_LOGGER = logging.getLogger(__name__)

API_KEY = "<API_KEY>"
NODE_PRO_ID = "<NODE_PRO_ID>"


async def main() -> None:
    """Create the aiohttp session and run the example."""
    logging.basicConfig(level=logging.INFO)
    async with ClientSession() as session:
        cloud_api = CloudAPI(API_KEY, session=session)

        # Get supported locations (by location):
        try:
            _LOGGER.info(await cloud_api.supported.countries())
            _LOGGER.info(await cloud_api.supported.states("USA"))
            _LOGGER.info(await cloud_api.supported.cities("USA", "Colorado"))
        except AirVisualError as err:
            _LOGGER.error("There was an error: %s", err)

        # Get supported locations (by station):
        try:
            _LOGGER.info(
                await cloud_api.supported.stations("USA", "Colorado", "Denver")
            )
        except UnauthorizedError as err:
            _LOGGER.error(err)
        except AirVisualError as err:
            _LOGGER.error("There was an error: %s", err)

        # Get data by nearest location (by IP):
        try:
            _LOGGER.info(await cloud_api.air_quality.nearest_city())
        except AirVisualError as err:
            _LOGGER.error("There was an error: %s", err)

        # Get data by nearest location (coordinates or explicit location):
        try:
            _LOGGER.info(
                await cloud_api.air_quality.nearest_city(
                    latitude=39.742599, longitude=-104.9942557
                )
            )
            _LOGGER.info(
                await cloud_api.air_quality.city(
                    city="Los Angeles", state="California", country="USA"
                )
            )
        except AirVisualError as err:
            _LOGGER.error("There was an error: %s", err)

        # Get data by nearest station (by IP):
        try:
            _LOGGER.info(await cloud_api.air_quality.nearest_station())
        except UnauthorizedError as err:
            _LOGGER.error(err)
        except AirVisualError as err:
            _LOGGER.error("There was an error: %s", err)

        # Get data by nearest station (by coordinates or explicit location):
        try:
            _LOGGER.info(
                await cloud_api.air_quality.nearest_station(
                    latitude=39.742599, longitude=-104.9942557
                )
            )
            _LOGGER.info(
                await cloud_api.air_quality.station(
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
            _LOGGER.info(await cloud_api.air_quality.ranking())
        except UnauthorizedError as err:
            _LOGGER.error(err)
        except AirVisualError as err:
            _LOGGER.error("There was an error: %s", err)

        # Get a Node/Pro unit via the Cloud API:
        _LOGGER.info(await cloud_api.node.get_by_node_id(NODE_PRO_ID))


asyncio.run(main())
