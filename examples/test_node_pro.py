"""Run an example against an AirVisual Node/Pro."""
import asyncio
import logging

from pyairvisual import NodeSamba
from pyairvisual.errors import NodeProError

_LOGGER = logging.getLogger(__name__)

NODE_PRO_IP_ADDRESS = "<NODE_PRO_IP_ADDRESS>"
NODE_PRO_PASSWORD = "<NODE_PRO_PASSWORD>"


async def main() -> None:
    """Create the aiohttp session and run the example."""
    logging.basicConfig(level=logging.INFO)

    async with NodeSamba(NODE_PRO_IP_ADDRESS, NODE_PRO_PASSWORD) as node:
        try:
            _LOGGER.info(await node.async_get_latest_measurements())
            _LOGGER.info(await node.async_get_history())
        except NodeProError as err:
            _LOGGER.error("There was an error: %s", err)


asyncio.run(main())
