"""Define tests for the "Data" object."""
# pylint: disable=redefined-outer-name,unused-import

import json

import aiohttp
import pytest

from pyairvisual import Client

from .const import (
    TEST_API_KEY, TEST_CITY, TEST_COUNTRY, TEST_LATITUDE, TEST_LONGITUDE,
    TEST_STATE, TEST_STATION_NAME)


@pytest.fixture(scope='module')
def fixture_nearest_city():
    """Return a /city or /nearest_city response."""
    return {
        "status": "success",
        "data": {
            "city": "Los Angeles",
            "state": "California",
            "country": "USA",
            "location": {
                "type": "Point",
                "coordinates": [-118.2417, 34.0669]
            },
            "current": {
                "weather": {
                    "ts": "2018-06-10T01:00:00.000Z",
                    "hu": 60,
                    "ic": "01d",
                    "pr": 1012,
                    "tp": 25,
                    "wd": 230,
                    "ws": 4.6
                },
                "pollution": {
                    "ts": "2018-06-10T00:00:00.000Z",
                    "aqius": 66,
                    "mainus": "p2",
                    "aqicn": 44,
                    "maincn": "p1"
                }
            }
        }
    }


@pytest.fixture(scope='module')
def fixture_nearest_station():
    """Return a /station or /nearest_station response."""
    return {
        "status": "success",
        "data": {
            "name":
                "US Embassy in Beijing",
            "local_name":
                "美国驻北京大使馆",
            "city":
                "Beijing",
            "state":
                "Beijing",
            "country":
                "China",
            "location": {
                "type": "Point",
                "coordinates": [116.466258, 39.954352]
            },
            "forecasts": [{
                "ts": "2017-09-04T03:00:00.000Z",
                "aqius": 174,
                "aqicn": 131,
                "tp": 26,
                "tp_min": 26,
                "pr": 1012,
                "hu": 64,
                "ws": 2,
                "wd": 196,
                "ic": "02d"
            }, {
                "ts": "2017-09-04T06:00:00.000Z",
                "aqius": 158,
                "aqicn": 94,
                "tp": 28,
                "tp_min": 28,
                "pr": 1010,
                "hu": 51,
                "ws": 4,
                "wd": 192,
                "ic": "10d"
            }, {
                "ts": "2017-09-07T00:00:00.000Z",
                "aqius": 158,
                "aqicn": 94,
                "tp": 21,
                "tp_min": 21,
                "pr": 1008,
                "hu": 55,
                "ws": 1,
                "wd": 338,
                "ic": "01d"
            }],
            "current": {
                "weather": {
                    "ts": "2017-09-04T02:00:00.000Z",
                    "tp": 24,
                    "pr": 1012,
                    "hu": 78,
                    "ws": 0,
                    "wd": 122,
                    "ic": "50d"
                },
                "pollution": {
                    "ts": "2017-09-04T02:00:00.000Z",
                    "aqius": 171,
                    "mainus": "p2",
                    "aqicn": 125,
                    "maincn": "p2",
                    "p2": {
                        "conc": 95,
                        "aqius": 171,
                        "aqicn": 125
                    }
                }
            },
            "history": {
                "weather": [{
                    "ts": "2017-09-04T02:00:00.000Z",
                    "tp": 24,
                    "pr": 1012,
                    "hu": 78,
                    "ws": 0,
                    "wd": 122,
                    "ic": "50d"
                }, {
                    "ts": "2017-09-04T01:00:00.000Z",
                    "tp": 23,
                    "pr": 1012,
                    "hu": 83,
                    "ws": 0,
                    "wd": 154,
                    "ic": "50d"
                }, {
                    "ts": "2017-09-02T02:00:00.000Z",
                    "tp": 24,
                    "pr": 1013,
                    "hu": 81,
                    "ws": 0,
                    "wd": 106,
                    "ic": "50d"
                }],
                "pollution": [{
                    "ts": "2017-09-04T02:00:00.000Z",
                    "aqius": 171,
                    "mainus": "p2",
                    "aqicn": 125,
                    "maincn": "p2",
                    "p2": {
                        "conc": 95,
                        "aqius": 171,
                        "aqicn": 125
                    }
                }, {
                    "ts": "2017-09-04T01:00:00.000Z",
                    "aqius": 169,
                    "mainus": "p2",
                    "aqicn": 119,
                    "maincn": "p2",
                    "p2": {
                        "conc": 90,
                        "aqius": 169,
                        "aqicn": 119
                    }
                }, {
                    "ts": "2017-09-02T03:00:00.000Z",
                    "aqius": 174,
                    "mainus": "p2",
                    "aqicn": 131,
                    "maincn": "p2",
                    "p2": {
                        "conc": 100,
                        "aqius": 174,
                        "aqicn": 131
                    }
                }]
            }
        }
    }


@pytest.fixture(scope='module')
def fixture_ranking():
    """Return a /city_ranking."""
    return {
        "status":
            "success",
        "data": [{
            "city": "Portland",
            "state": "Oregon",
            "country": "USA",
            "ranking": {
                "current_aqi": 183,
                "current_aqi_cn": 154
            }
        }, {
            "city": "Eugene",
            "state": "Oregon",
            "country": "USA",
            "ranking": {
                "current_aqi": 151,
                "current_aqi_cn": 77
            }
        }, {
            "city": "Richards Bay",
            "state": "KwaZulu-Natal",
            "country": "South Africa",
            "ranking": {
                "current_aqi": 3,
                "current_aqi_cn": 3,
                "last_aqi": 5,
                "last_aqi_cn": 5
            }
        }]
    }


@pytest.mark.asyncio
async def test_endpoints(
        aresponses, event_loop, fixture_nearest_city, fixture_nearest_station,
        fixture_ranking):
    """Test all endpoints."""
    aresponses.add(
        'api.airvisual.com', '/v2/nearest_city', 'get',
        aresponses.Response(text=json.dumps(fixture_nearest_city), status=200))
    aresponses.add(
        'api.airvisual.com', '/v2/city', 'get',
        aresponses.Response(text=json.dumps(fixture_nearest_city), status=200))
    aresponses.add(
        'api.airvisual.com', '/v2/nearest_station', 'get',
        aresponses.Response(
            text=json.dumps(fixture_nearest_station), status=200))
    aresponses.add(
        'api.airvisual.com', '/v2/station', 'get',
        aresponses.Response(
            text=json.dumps(fixture_nearest_station), status=200))
    aresponses.add(
        'api.airvisual.com', '/v2/city_ranking', 'get',
        aresponses.Response(text=json.dumps(fixture_ranking), status=200))

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = Client(TEST_API_KEY, websession)

        data = await client.api.nearest_city(
            latitude=TEST_LATITUDE, longitude=TEST_LONGITUDE)
        assert data['city'] == 'Los Angeles'

        data = await client.api.city(TEST_CITY, TEST_STATE, TEST_COUNTRY)
        assert data['city'] == 'Los Angeles'

        data = await client.api.nearest_station(
            latitude=TEST_LATITUDE, longitude=TEST_LONGITUDE)
        assert data['name'] == 'US Embassy in Beijing'

        data = await client.api.station(
            TEST_STATION_NAME, TEST_CITY, TEST_STATE, TEST_COUNTRY)
        assert data['name'] == 'US Embassy in Beijing'

        data = await client.api.ranking()
        assert len(data) == 3
