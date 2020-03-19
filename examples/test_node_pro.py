"""Run an example against an AirVisual Node/Pro."""
import asyncio
import logging

from aiohttp import ClientSession

from pyairvisual import Client
from pyairvisual.errors import AirVisualError

_LOGGER = logging.getLogger(__name__)

NODE_PRO_ID = "<NODE_PRO_ID>"

NODE_PRO_IP_ADDRESS = "172.16.11.180"
NODE_PRO_PASSWORD = "j9h46kar"


async def main() -> None:
    """Create the aiohttp session and run the example."""
    logging.basicConfig(level=logging.INFO)
    async with ClientSession() as websession:
        client = Client(websession)

        # Get data from the cloud API:
        # try:
        #     _LOGGER.info(await client.node.from_cloud_api(NODE_PRO_ID))
        # except AirVisualError as err:
        #     _LOGGER.error("There was an error: %s", err)

        # Get data from the local Samba share on the unit:
        try:
            _LOGGER.info(
                await client.node.from_samba(
                    NODE_PRO_IP_ADDRESS,
                    NODE_PRO_PASSWORD,
                    include_trends=False,
                ),
            )
        except AirVisualError as err:
            _LOGGER.error("There was an error: %s", err)


asyncio.get_event_loop().run_until_complete(main())
