"""Define tests for the "Supported" object."""
# pylint: disable=redefined-outer-name,unused-import

import json

import aiohttp
import pytest

from pyairvisual import Client

from .const import TEST_API_KEY, TEST_CITY, TEST_COUNTRY, TEST_STATE


@pytest.fixture(scope='module')
def fixture_cities():
    """Return a /cities response."""
    return {
        "status":
            "success",
        "data": [{
            "city": "Boulder"
        }, {
            "city": "Centennial"
        }, {
            "city": "Colorado Springs"
        }, {
            "city": "Conifer"
        }, {
            "city": "Cortez"
        }, {
            "city": "Delta"
        }, {
            "city": "Denver"
        }, {
            "city": "Durango"
        }, {
            "city": "Estes Park"
        }, {
            "city": "Fort Collins"
        }, {
            "city": "Golden"
        }, {
            "city": "Gothic"
        }, {
            "city": "Grand Junction"
        }, {
            "city": "Greeley"
        }, {
            "city": "Ignacio"
        }, {
            "city": "Littleton"
        }, {
            "city": "Louisville"
        }, {
            "city": "Manitou Springs"
        }, {
            "city": "Meeker"
        }, {
            "city": "Mesa Verde National Park"
        }, {
            "city": "Morrison"
        }, {
            "city": "Pagosa Springs"
        }, {
            "city": "Palisade"
        }, {
            "city": "Rangely"
        }, {
            "city": "Rifle"
        }, {
            "city": "U.S. Air Force Academy"
        }, {
            "city": "Watkins"
        }]
    }


@pytest.fixture(scope='module')
def fixture_countries():
    """Return a /countries response."""
    return {
        "status":
            "success",
        "data": [{
            "country": "Afghanistan"
        }, {
            "country": "Andorra"
        }, {
            "country": "Australia"
        }, {
            "country": "Austria"
        }, {
            "country": "Bahrain"
        }, {
            "country": "Bangladesh"
        }, {
            "country": "Belgium"
        }, {
            "country": "Bosnia Herzegovina"
        }, {
            "country": "Brazil"
        }, {
            "country": "Bulgaria"
        }, {
            "country": "Cambodia"
        }, {
            "country": "Canada"
        }, {
            "country": "Chile"
        }, {
            "country": "China"
        }, {
            "country": "Colombia"
        }, {
            "country": "Croatia"
        }, {
            "country": "Cyprus"
        }, {
            "country": "Czech Republic"
        }, {
            "country": "Denmark"
        }, {
            "country": "Egypt"
        }, {
            "country": "Estonia"
        }, {
            "country": "Ethiopia"
        }, {
            "country": "Finland"
        }, {
            "country": "France"
        }, {
            "country": "Germany"
        }, {
            "country": "Greece"
        }, {
            "country": "Hong Kong"
        }, {
            "country": "Hungary"
        }, {
            "country": "Iceland"
        }, {
            "country": "India"
        }, {
            "country": "Indonesia"
        }, {
            "country": "Iran"
        }, {
            "country": "Ireland"
        }, {
            "country": "Israel"
        }, {
            "country": "Italy"
        }, {
            "country": "Japan"
        }, {
            "country": "Kosovo"
        }, {
            "country": "Kuwait"
        }, {
            "country": "Latvia"
        }, {
            "country": "Lithuania"
        }, {
            "country": "Macedonia"
        }, {
            "country": "Malaysia"
        }, {
            "country": "Malta"
        }, {
            "country": "Mexico"
        }, {
            "country": "Mongolia"
        }, {
            "country": "Morocco"
        }, {
            "country": "Nepal"
        }, {
            "country": "Netherlands"
        }, {
            "country": "New Zealand"
        }, {
            "country": "Nigeria"
        }, {
            "country": "Norway"
        }, {
            "country": "Pakistan"
        }, {
            "country": "Peru"
        }, {
            "country": "Philippines"
        }, {
            "country": "Poland"
        }, {
            "country": "Portugal"
        }, {
            "country": "Puerto Rico"
        }, {
            "country": "Qatar"
        }, {
            "country": "Russia"
        }, {
            "country": "Saudi Arabia"
        }, {
            "country": "Serbia"
        }, {
            "country": "Singapore"
        }, {
            "country": "Slovakia"
        }, {
            "country": "Slovenia"
        }, {
            "country": "South Africa"
        }, {
            "country": "South Korea"
        }, {
            "country": "Spain"
        }, {
            "country": "Sri Lanka"
        }, {
            "country": "Sweden"
        }, {
            "country": "Switzerland"
        }, {
            "country": "Taiwan"
        }, {
            "country": "Thailand"
        }, {
            "country": "Turkey"
        }, {
            "country": "USA"
        }, {
            "country": "Uganda"
        }, {
            "country": "Ukraine"
        }, {
            "country": "United Arab Emirates"
        }, {
            "country": "United Kingdom"
        }, {
            "country": "Vietnam"
        }]
    }


@pytest.fixture(scope='module')
def fixture_states():
    """Return a /states response."""
    return {
        "status":
            "success",
        "data": [{
            "state": "New South Wales"
        }, {
            "state": "Queensland"
        }, {
            "state": "South Australia"
        }, {
            "state": "Tasmania"
        }, {
            "state": "Victoria"
        }, {
            "state": "Western Australia"
        }]
    }


@pytest.fixture(scope='module')
def fixture_stations():
    """Return a /stations response."""
    return {
        "status":
            "success",
        "data": [{
            "location": {
                "type": "Point",
                "coordinates": [116.466258, 39.954352]
            },
            "station": "US Embassy in Beijing"
        }, {
            "location": {
                "type": "Point",
                "coordinates": [116.2148532181, 40.0078007235]
            },
            "station": "Botanical Garden"
        }]
    }


@pytest.mark.asyncio
async def test_endpoints(  # pylint: disable=too-many-arguments
        aresponses, event_loop, fixture_cities, fixture_countries,
        fixture_states, fixture_stations):
    """Test all endpoints."""
    aresponses.add(
        'api.airvisual.com', '/v2/cities', 'get',
        aresponses.Response(text=json.dumps(fixture_cities), status=200))
    aresponses.add(
        'api.airvisual.com', '/v2/countries', 'get',
        aresponses.Response(text=json.dumps(fixture_countries), status=200))
    aresponses.add(
        'api.airvisual.com', '/v2/states', 'get',
        aresponses.Response(text=json.dumps(fixture_states), status=200))
    aresponses.add(
        'api.airvisual.com', '/v2/stations', 'get',
        aresponses.Response(text=json.dumps(fixture_stations), status=200))

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = Client(TEST_API_KEY, websession)

        cities = await client.supported.cities(TEST_COUNTRY, TEST_STATE)
        assert cities == [d['city'] for d in fixture_cities['data']]

        countries = await client.supported.countries()
        assert countries == [d['country'] for d in fixture_countries['data']]

        states = await client.supported.states(TEST_COUNTRY)
        assert states == [d['state'] for d in fixture_states['data']]

        stations = await client.supported.stations(
            TEST_CITY, TEST_STATE, TEST_COUNTRY)
        assert stations == [station for station in fixture_stations['data']]
