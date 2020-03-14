"""Run an example against an AirVisual Node/Pro."""
import asyncio
import logging

from aiohttp import ClientSession

from pyairvisual import Client
from pyairvisual.errors import AirVisualError

_LOGGER = logging.getLogger(__name__)


async def main() -> None:
    """Create the aiohttp session and run the example."""
    logging.basicConfig(level=logging.INFO)
    async with ClientSession() as websession:
        client = Client(websession)

        # Get data from the cloud API:
        try:
            _LOGGER.info(await client.node.from_cloud_api("L7L2Yz4kvEHNx3NFT"))
        except AirVisualError as err:
            _LOGGER.error("There was an error: %s", err)


asyncio.get_event_loop().run_until_complete(main())
