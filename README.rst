☀️ pyairvisual: a thin Python wrapper for the AirVisual© API
===========================================================

.. image:: https://travis-ci.org/bachya/pyairvisual.svg?branch=master
  :target: https://travis-ci.org/bachya/pyairvisual

.. image:: https://img.shields.io/pypi/v/pyairvisual.svg
  :target: https://pypi.python.org/pypi/pyairvisual

.. image:: https://img.shields.io/pypi/pyversions/pyairvisual.svg
  :target: https://pypi.python.org/pypi/pyairvisual

.. image:: https://img.shields.io/pypi/l/pyairvisual.svg
  :target: https://github.com/bachya/pyairvisual/blob/master/LICENSE

.. image:: https://codecov.io/gh/bachya/pyairvisual/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/bachya/pyairvisual

.. image:: https://api.codeclimate.com/v1/badges/948e4e3c84e5c49826f1/maintainability
   :target: https://codeclimate.com/github/bachya/pyairvisual/maintainability
   :alt: Maintainability

.. image:: https://img.shields.io/badge/SayThanks-!-1EAEDB.svg
  :target: https://saythanks.io/to/bachya

pyairvisual is a simple, clean, well-tested library for interacting with
`AirVisual <https://www.airvisual.com/>`_ to retrieve air quality information.

☀️ PLEASE READ: 1.0.0 and Beyond
================================

Version 1.0.0 of pyairvisual makes several breaking, but necessary changes:

* Moves the underlying library from
  `Requests <http://docs.python-requests.org/en/master/>`_ to
  `aiohttp <https://aiohttp.readthedocs.io/en/stable/>`_
* Changes the entire library to use :code:`asyncio`
* Makes 3.5 the minimum version of Python required

If you wish to continue using the previous, synchronous version of
pyairvisual, make sure to pin version 1.0.0.

💧 Installation
===============

.. code-block:: bash

  $ pip install pyairvisual

💧 Example
==========

pyairvisual starts within an
`aiohttp <https://aiohttp.readthedocs.io/en/stable/>`_ :code:`ClientSession`:

.. code-block:: python

  import asyncio

  from aiohttp import ClientSession

  from pyairvisual import Client


  async def main() -> None:
      """Create the aiohttp session and run the example."""
      async with ClientSession() as websession:
          await run(websession)


  async def run(websession):
      """Run."""
      # YOUR CODE HERE

  asyncio.get_event_loop().run_until_complete(main())

Create a client:

.. code-block:: python

  client = Client('<YOUR AIRVISUAL API KEY>')

Then, get to work:

.. code-block:: python

  # Get data based on the city nearest to your IP address:
  data = await client.data.nearest_city()

  # ...or get data based on the city nearest to a latitude/longitude:
  data = await client.data.nearest_city(
    latitude=39.742599, longitude=-104.9942557)

  # ...or get it explicitly:
  data = await client.data.city(
    city='Los Angeles', state='California', country='USA')

  # If you have the appropriate API key, you can also get data based on station
  # (nearest or explicit):
  data = await client.data.nearest_station()
  data = await client.data.nearest_station(
    latitude=39.742599, longitude=-104.9942557)
  data = await client.data.station(
      station='US Embassy in Beijing',
      city='Beijing',
      state='Beijing',
      country='China')

  # With the appropriate API key, you can get an air quality ranking:
  data = client.data.ranking()

  # Lastly, pyairvisual gives you several methods to look locations up:
  countries = await client.supported.countries()
  states = await client.supported.states('USA')
  cities = await client.supported.cities('USA', 'Colorado')
  stations = await client.supported.stations('USA', 'Colorado', 'Denver')

Check out `example.py`, the tests, and the source files themselves for method
signatures and more examples.

💧 Contributing
===============

#. `Check for open features/bugs <https://github.com/bachya/regenmaschine/issues>`_
   or `initiate a discussion on one <https://github.com/bachya/regenmaschine/issues/new>`_.
#. `Fork the repository <https://github.com/bachya/regenmaschine/fork>`_.
#. Install the dev environment: :code:`make init`.
#. Enter the virtual environment: :code:`pipenv shell`
#. Code your new feature or bug fix.
#. Write a test that covers your new functionality.
#. Run tests: :code:`make test`
#. Build new docs: :code:`make docs`
#. Add yourself to AUTHORS.rst.
#. Submit a pull request!
