# ☀️ pyairvisual: a thin Python wrapper for the AirVisual© API

[![CI](https://github.com/bachya/pyairvisual/workflows/CI/badge.svg)](https://github.com/bachya/pyairvisual/actions)
[![PyPi](https://img.shields.io/pypi/v/pyairvisual.svg)](https://pypi.python.org/pypi/pyairvisual)
[![Version](https://img.shields.io/pypi/pyversions/pyairvisual.svg)](https://pypi.python.org/pypi/pyairvisual)
[![License](https://img.shields.io/pypi/l/pyairvisual.svg)](https://github.com/bachya/pyairvisual/blob/master/LICENSE)
[![Code Coverage](https://codecov.io/gh/bachya/pyairvisual/branch/master/graph/badge.svg)](https://codecov.io/gh/bachya/pyairvisual)
[![Maintainability](https://api.codeclimate.com/v1/badges/948e4e3c84e5c49826f1/maintainability)](https://codeclimate.com/github/bachya/pyairvisual/maintainability)
[![Say Thanks](https://img.shields.io/badge/SayThanks-!-1EAEDB.svg)](https://saythanks.io/to/bachya)

`pyairvisual` is a simple, clean, well-tested library for interacting with
[AirVisual](https://www.airvisual.com/) to retrieve air quality information.

# PLEASE READ: Version 2.0.0 and Beyond

Version 2.0.0 of `pyairvisual` makes several breaking, but necessary changes:

* Moves the underlying library from
  [Requests](http://docs.python-requests.org/en/master/) to
  [aiohttp](https://aiohttp.readthedocs.io/en/stable/)
* Changes the entire library to use `asyncio`
* Makes 3.6 the minimum version of Python required

If you wish to continue using the previous, synchronous version of
`pyairvisual`, make sure to pin version 1.0.0.

# Python Versions

`pyairvisual` is currently supported on:

* Python 3.6
* Python 3.7
* Python 3.8

# Installation

```python
pip install pyairvisual
```

# API Key

You can get an AirVisual API key from
[the AirVisual API site](https://www.airvisual.com/user/api). Depending on
the plan you choose, more functionality will be available from the API:

## Community

The Community Plan gives access to:

* List supported countries
* List supported states
* List supported cities
* Get data from the nearest city based on IP address
* Get data from the nearest city based on latitude/longitude
* Get data from a specific city

## Startup

The Startup Plan gives access to:

* List supported stations in a city
* Get data from the nearest station based on IP address
* Get data from the nearest station based on latitude/longitude
* Get data from a specific station

## Enterprise

The Enterprise Plan gives access to:

* Get a global city ranking of air quality

# Usage

`pyairvisual` starts within an
[aiohttp](https://aiohttp.readthedocs.io/en/stable/) `ClientSession`:

```python
import asyncio

from aiohttp import ClientSession

from pyairvisual import Client


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as websession:
      # YOUR CODE HERE


asyncio.get_event_loop().run_until_complete(main())
```

Create a client and get to work:

```python
import asyncio

from aiohttp import ClientSession

from pyairvisual import Client


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as websession:
    # If an API key isn't provided, only Nodes can be queried; everything else
    # requires an API key:
    client = Client(websession, api_key='<YOUR AIRVISUAL API KEY>')

    # Get data based on the city nearest to your IP address:
    data = await client.data.nearest_city()

    # ...or get data based on the city nearest to a latitude/longitude:
    data = await client.data.nearest_city(
        latitude=39.742599, longitude=-104.9942557)

    # ...or get it explicitly:
    data = await client.data.city(
        city='Los Angeles', state='California', country='USA')

    # If you have the appropriate API key, you can also get data based on
    # station (nearest or explicit):
    data = await client.data.nearest_station()
    data = await client.data.nearest_station(
        latitude=39.742599, longitude=-104.9942557)
    data = await client.data.station(
        station='US Embassy in Beijing',
        city='Beijing',
        state='Beijing',
        country='China')

    # With the appropriate API key, you can get an air quality ranking:
    data = await client.data.ranking()

    # pyairvisual gives you several methods to look locations up:
    countries = await client.supported.countries()
    states = await client.supported.states('USA')
    cities = await client.supported.cities('USA', 'Colorado')
    stations = await client.supported.stations('USA', 'Colorado', 'Denver')

    # AirVisual Nodes can also be queried by ID
    data = await client.api.node('12345abcdef')


asyncio.get_event_loop().run_until_complete(main())
```

Check out `example.py`, the tests, and the source files themselves for method
signatures and more examples.

# Contributing

1. [Check for open features/bugs](https://github.com/bachya/pyairvisual/issues)
  or [initiate a discussion on one](https://github.com/bachya/pyairvisual/issues/new).
2. [Fork the repository](https://github.com/bachya/pyairvisual/fork).
3. (_optional, but highly recommended_) Create a virtual environment: `python3 -m venv .venv`
4. (_optional, but highly recommended_) Enter the virtual environment: `source ./venv/bin/activate`
5. Install the dev environment: `script/setup`
6. Code your new feature or bug fix.
7. Write tests that cover your new functionality.
8. Run tests and ensure 100% code coverage: `script/test`
9. Update `README.md` with any new documentation.
10. Add yourself to `AUTHORS.md`.
11. Submit a pull request!
