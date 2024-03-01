"""Run an example against an AirVisual Node/Pro."""

import asyncio
import logging

from pyairvisual.node import NodeProError, NodeSamba

_LOGGER = logging.getLogger(__name__)

NODE_PRO_IP_ADDRESS = "<NODE_PRO_IP_ADDRESS>"
NODE_PRO_PASSWORD = "<NODE_PRO_PASSWORD>"  # noqa: S105


async def main() -> None:
    """Create the aiohttp session and run the example."""
    logging.basicConfig(level=logging.INFO)

    try:
        async with NodeSamba(NODE_PRO_IP_ADDRESS, NODE_PRO_PASSWORD) as node:
            _LOGGER.info(await node.async_get_latest_measurements())
            _LOGGER.info(await node.async_get_history())
    except NodeProError as err:
        _LOGGER.error(err)


asyncio.run(main())
