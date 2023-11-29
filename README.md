# ☀️ pyairvisual: a thin Python wrapper for the AirVisual© API

[![CI][ci-badge]][ci]
[![PyPI][pypi-badge]][pypi]
[![Version][version-badge]][version]
[![License][license-badge]][license]
[![Code Coverage][codecov-badge]][codecov]
[![Maintainability][maintainability-badge]][maintainability]

<a href="https://www.buymeacoffee.com/bachya1208P" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

`pyairvisual` is a simple, clean, well-tested library for interacting with
[AirVisual][airvisual] to retrieve air quality information.

- [Python Versions](#python-versions)
- [Installation](#installation)
- [API Key](#api-key)
  - [Community](#community)
  - [Startup](#startup)
  - [Enterprise](#enterprise)
- [Usage](#usage)
  - [Using the Cloud API](#using-the-cloud-api)
  - [Working with Node/Pro Units](#working-with-node-pro-units)
- [Contributing](#contributing)

# Python Versions

`pyairvisual` is currently supported on:

- Python 3.10
- Python 3.11
- Python 3.12

# Installation

```bash
pip install pyairvisual
```

# API Key

You can get an AirVisual API key from [the AirVisual API site][airvisual-api].
Depending on the plan you choose, more functionality will be available from the API:

## Community

The Community Plan gives access to:

- List supported countries
- List supported states
- List supported cities
- Get data from the nearest city based on IP address
- Get data from the nearest city based on latitude/longitude
- Get data from a specific city

## Startup

The Startup Plan gives access to:

- List supported stations in a city
- Get data from the nearest station based on IP address
- Get data from the nearest station based on latitude/longitude
- Get data from a specific station

## Enterprise

The Enterprise Plan gives access to:

- Get a global city ranking of air quality

# Usage

## Using the Cloud API

```python
import asyncio

from pyairvisual.cloud_api import CloudAPI


async def main() -> None:
    """Run!"""
    cloud_api = CloudAPI("<YOUR_AIRVISUAL_API_KEY>")

    # Get data based on the city nearest to your IP address:
    data = await cloud_api.air_quality.nearest_city()

    # ...or get data based on the city nearest to a latitude/longitude:
    data = await cloud_api.air_quality.nearest_city(
        latitude=39.742599, longitude=-104.9942557
    )

    # ...or get it explicitly:
    data = await cloud_api.air_quality.city(
        city="Los Angeles", state="California", country="USA"
    )

    # If you have the appropriate API key, you can also get data based on
    # station (nearest or explicit):
    data = await cloud_api.air_quality.nearest_station()
    data = await cloud_api.air_quality.nearest_station(
        latitude=39.742599, longitude=-104.9942557
    )
    data = await cloud_api.air_quality.station(
        station="US Embassy in Beijing",
        city="Beijing",
        state="Beijing",
        country="China",
    )

    # With the appropriate API key, you can get an air quality ranking:
    data = await cloud_api.air_quality.ranking()

    # pyairvisual gives you several methods to look locations up:
    countries = await cloud_api.supported.countries()
    states = await cloud_api.supported.states("USA")
    cities = await cloud_api.supported.cities("USA", "Colorado")
    stations = await cloud_api.supported.stations("USA", "Colorado", "Denver")


asyncio.run(main())
```

By default, the library creates a new connection to AirVisual with each coroutine. If
you are calling a large number of coroutines (or merely want to squeeze out every second
of runtime savings possible), an [`aiohttp`][aiohttp] `ClientSession` can be used for
connection pooling:

```python
import asyncio

from aiohttp import ClientSession

from pyairvisual.cloud_api import CloudAPI


async def main() -> None:
    """Run!"""
    async with ClientSession() as session:
        cloud_api = CloudAPI("<YOUR_AIRVISUAL_API_KEY>", session=session)

        # ...


asyncio.run(main())
```

## Working with Node/Pro Units

`pyairvisual` also allows users to interact with [Node/Pro units][airvisual-pro], both via
the cloud API:

```python
import asyncio

from aiohttp import ClientSession

from pyairvisual.cloud_api import CloudAPI


async def main() -> None:
    """Run!"""
    cloud_api = CloudAPI("<YOUR_AIRVISUAL_API_KEY>")

    # The Node/Pro unit ID can be retrieved from the "API" section of the cloud
    # dashboard:
    data = await cloud_api.node.get_by_node_id("<NODE_ID>")


asyncio.run(main())
```

...or over the local network via Samba (the unit password can be found
[on the device itself][airvisual-samba-instructions]):

```python
import asyncio

from aiohttp import ClientSession

from pyairvisual.node import NodeSamba


async def main() -> None:
    """Run!"""
    async with NodeSamba("<IP_ADDRESS_OR_HOST>", "<PASSWORD>") as node:
        measurements = await node.async_get_latest_measurements()

        # Can take some optional parameters:
        #   1. include_trends: include trends (defaults to True)
        #   2. measurements_to_use: the number of measurements to use when calculating
        #      trends (defaults to -1, which means "use all measurements")
        history = await node.async_get_history()


asyncio.run(main())
```

Check out the examples, the tests, and the source files themselves for method
signatures and more examples.

# Contributing

Thanks to all of [our contributors][contributors] so far!

1. [Check for open features/bugs][issues] or [initiate a discussion on one][new-issue].
2. [Fork the repository][fork].
3. (_optional, but highly recommended_) Create a virtual environment: `python3 -m venv .venv`
4. (_optional, but highly recommended_) Enter the virtual environment: `source ./.venv/bin/activate`
5. Install the dev environment: `script/setup`
6. Code your new feature or bug fix on a new branch.
7. Write tests that cover your new functionality.
8. Run tests and ensure 100% code coverage: `poetry run pytest --cov pyairvisual tests`
9. Update `README.md` with any new documentation.
10. Submit a pull request!

[aiohttp]: https://github.com/aio-libs/aiohttp
[airvisual]: https://www.airvisual.com/
[airvisual-api]: https://www.airvisual.com/user/api
[airvisual-pro]: https://www.airvisual.com/air-quality-monitor
[airvisual-samba-instructions]: https://support.airvisual.com/en/articles/3029331-download-the-airvisual-node-pro-s-data-using-samba
[ci-badge]: https://github.com/bachya/pyairvisual/workflows/CI/badge.svg
[ci]: https://github.com/bachya/pyairvisual/actions
[codecov-badge]: https://codecov.io/gh/bachya/pyairvisual/branch/dev/graph/badge.svg
[codecov]: https://codecov.io/gh/bachya/pyairvisual
[contributors]: https://github.com/bachya/pyairvisual/graphs/contributors
[fork]: https://github.com/bachya/pyairvisual/fork
[issues]: https://github.com/bachya/pyairvisual/issues
[license-badge]: https://img.shields.io/pypi/l/pyairvisual.svg
[license]: https://github.com/bachya/pyairvisual/blob/main/LICENSE
[maintainability-badge]: https://api.codeclimate.com/v1/badges/948e4e3c84e5c49826f1/maintainability
[maintainability]: https://codeclimate.com/github/bachya/pyairvisual/maintainability
[new-issue]: https://github.com/bachya/pyairvisual/issues/new
[new-issue]: https://github.com/bachya/pyairvisual/issues/new
[pypi-badge]: https://img.shields.io/pypi/v/pyairvisual.svg
[pypi]: https://pypi.python.org/pypi/pyairvisual
[version-badge]: https://img.shields.io/pypi/pyversions/pyairvisual.svg
[version]: https://pypi.python.org/pypi/pyairvisual
