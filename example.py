"""Run an example script to quickly test."""
import asyncio

from aiohttp import ClientSession

from pyairvisual import Client
from pyairvisual.errors import RequestError, UnauthorizedError


async def data(client: Client) -> None:
    """Output data-related information."""
    print('DATA FOR CITY CLOSEST TO THIS IP ADDRESS:')
    info = await client.data.nearest_city()
    print(info)

    print()
    print('DATA FOR CITY CLOSEST TO 39.742599,-104.9942557:')
    info = await client.data.nearest_city(
        latitude=39.742599, longitude=-104.9942557)
    print(info)

    print()
    print('DATA FOR LOS ANGELES:')
    info = await client.data.city(
        city='Los Angeles', state='California', country='USA')
    print(info)

    try:
        print()
        print('DATA FOR STATION CLOSEST TO THIS IP ADDRESS:')
        info = await client.data.nearest_station()
        print(info)
    except UnauthorizedError:
        print("You don't have permission to access this endpoint")

    try:
        print()
        print('DATA FOR STATION CLOSEST TO 39.742599,-104.9942557:')
        info = await client.data.nearest_station(
            latitude=39.742599, longitude=-104.9942557)
        print(info)
    except UnauthorizedError:
        print("You don't have permission to access this endpoint")

    try:
        print()
        print('DATA FOR STATION: US EMBASSY IN BEIJING:')
        info = await client.data.station(
            station='US Embassy in Beijing',
            city='Beijing',
            state='Beijing',
            country='China')
        print(info)
    except UnauthorizedError:
        print("You don't have permission to access this endpoint")

    try:
        print()
        print('AQI RANKING:')
        info = await client.data.ranking()
        print(info)
    except UnauthorizedError:
        print("You don't have permission to access this endpoint")


async def supported(client: Client) -> None:
    """Output zone-related information."""
    print('SUPPORTED COUNTRIES:')
    countries = await client.supported.countries()
    print(countries)

    print()
    print('SUPPORTED STATES IN U.S.A:')
    states = await client.supported.states('USA')
    print(states)

    print()
    print('SUPPORTED CITIES IN COLORADO:')
    cities = await client.supported.cities('USA', 'Colorado')
    print(cities)

    try:
        print()
        print('SUPPORTED STATIONS IN DENVER:')
        stations = await client.supported.stations('USA', 'Colorado', 'Denver')
        print(stations)
    except UnauthorizedError:
        print("You don't have permission to access this endpoint")


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as websession:
        await run(websession)


async def run(websession):
    """Run."""
    try:
        # Create a client:
        client = Client('1234567890abcdefg', websession)

        # Work with supported locations:
        await supported(client)

        # Work with air quality data:
        print()
        await data(client)
    except RequestError as err:
        print(err)


asyncio.get_event_loop().run_until_complete(main())
