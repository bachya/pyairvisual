"""Define fixtures for the "API" object."""
import pytest


@pytest.fixture()
def fixture_city():
    """Return a /city or /nearest_city response."""
    return {
        "status": "success",
        "data": {
            "city": "Los Angeles",
            "state": "California",
            "country": "USA",
            "location": {"type": "Point", "coordinates": [-118.2417, 34.0669]},
            "current": {
                "weather": {
                    "ts": "2018-06-10T01:00:00.000Z",
                    "hu": 60,
                    "ic": "01d",
                    "pr": 1012,
                    "tp": 25,
                    "wd": 230,
                    "ws": 4.6,
                },
                "pollution": {
                    "ts": "2018-06-10T00:00:00.000Z",
                    "aqius": 66,
                    "mainus": "p2",
                    "aqicn": 44,
                    "maincn": "p1",
                },
            },
        },
    }


@pytest.fixture()
def fixture_node():
    """Return a /node response."""
    return {
        "settings": {"node_name": "hlubocepy"},
        "current": {
            "ts": "2019-02-15T23:32:49.573Z",
            "tp": 2.3,
            "hm": 73,
            "p2": 35,
            "co": 479,
        },
        "historical": {
            "instant": [
                {
                    "ts": "2019-02-15T23:32:49.573Z",
                    "tp": 2.3,
                    "hm": 73,
                    "p2": 35,
                    "co": 479,
                }
            ],
            "daily": [
                {
                    "p2_sum": 3321,
                    "p2_count": 204,
                    "p1_sum": 0,
                    "p1_count": 204,
                    "p01_sum": 0,
                    "p01_count": 204,
                    "co_sum": 93265,
                    "co_count": 204,
                    "hm_sum": 11906,
                    "hm_count": 204,
                    "tp_sum": 1535.0999999999997,
                    "tp_count": 204,
                    "voc_sum": 0,
                    "voc_count": 204,
                    "ts": "2019-02-15T00:00:00.000Z",
                    "outdoor_station": {},
                }
            ],
        },
    }


@pytest.fixture()
def fixture_station():
    """Return a /station or /nearest_station response."""
    return {
        "status": "success",
        "data": {
            "name": "US Embassy in Beijing",
            "local_name": "美国驻北京大使馆",
            "city": "Beijing",
            "state": "Beijing",
            "country": "China",
            "location": {"type": "Point", "coordinates": [116.466258, 39.954352]},
            "forecasts": [
                {
                    "ts": "2017-09-04T03:00:00.000Z",
                    "aqius": 174,
                    "aqicn": 131,
                    "tp": 26,
                    "tp_min": 26,
                    "pr": 1012,
                    "hu": 64,
                    "ws": 2,
                    "wd": 196,
                    "ic": "02d",
                },
                {
                    "ts": "2017-09-04T06:00:00.000Z",
                    "aqius": 158,
                    "aqicn": 94,
                    "tp": 28,
                    "tp_min": 28,
                    "pr": 1010,
                    "hu": 51,
                    "ws": 4,
                    "wd": 192,
                    "ic": "10d",
                },
                {
                    "ts": "2017-09-07T00:00:00.000Z",
                    "aqius": 158,
                    "aqicn": 94,
                    "tp": 21,
                    "tp_min": 21,
                    "pr": 1008,
                    "hu": 55,
                    "ws": 1,
                    "wd": 338,
                    "ic": "01d",
                },
            ],
            "current": {
                "weather": {
                    "ts": "2017-09-04T02:00:00.000Z",
                    "tp": 24,
                    "pr": 1012,
                    "hu": 78,
                    "ws": 0,
                    "wd": 122,
                    "ic": "50d",
                },
                "pollution": {
                    "ts": "2017-09-04T02:00:00.000Z",
                    "aqius": 171,
                    "mainus": "p2",
                    "aqicn": 125,
                    "maincn": "p2",
                    "p2": {"conc": 95, "aqius": 171, "aqicn": 125},
                },
            },
            "history": {
                "weather": [
                    {
                        "ts": "2017-09-04T02:00:00.000Z",
                        "tp": 24,
                        "pr": 1012,
                        "hu": 78,
                        "ws": 0,
                        "wd": 122,
                        "ic": "50d",
                    },
                    {
                        "ts": "2017-09-04T01:00:00.000Z",
                        "tp": 23,
                        "pr": 1012,
                        "hu": 83,
                        "ws": 0,
                        "wd": 154,
                        "ic": "50d",
                    },
                    {
                        "ts": "2017-09-02T02:00:00.000Z",
                        "tp": 24,
                        "pr": 1013,
                        "hu": 81,
                        "ws": 0,
                        "wd": 106,
                        "ic": "50d",
                    },
                ],
                "pollution": [
                    {
                        "ts": "2017-09-04T02:00:00.000Z",
                        "aqius": 171,
                        "mainus": "p2",
                        "aqicn": 125,
                        "maincn": "p2",
                        "p2": {"conc": 95, "aqius": 171, "aqicn": 125},
                    },
                    {
                        "ts": "2017-09-04T01:00:00.000Z",
                        "aqius": 169,
                        "mainus": "p2",
                        "aqicn": 119,
                        "maincn": "p2",
                        "p2": {"conc": 90, "aqius": 169, "aqicn": 119},
                    },
                    {
                        "ts": "2017-09-02T03:00:00.000Z",
                        "aqius": 174,
                        "mainus": "p2",
                        "aqicn": 131,
                        "maincn": "p2",
                        "p2": {"conc": 100, "aqius": 174, "aqicn": 131},
                    },
                ],
            },
        },
    }


@pytest.fixture()
def fixture_ranking():
    """Return a /city_ranking."""
    return {
        "status": "success",
        "data": [
            {
                "city": "Portland",
                "state": "Oregon",
                "country": "USA",
                "ranking": {"current_aqi": 183, "current_aqi_cn": 154},
            },
            {
                "city": "Eugene",
                "state": "Oregon",
                "country": "USA",
                "ranking": {"current_aqi": 151, "current_aqi_cn": 77},
            },
            {
                "city": "Richards Bay",
                "state": "KwaZulu-Natal",
                "country": "South Africa",
                "ranking": {
                    "current_aqi": 3,
                    "current_aqi_cn": 3,
                    "last_aqi": 5,
                    "last_aqi_cn": 5,
                },
            },
        ],
    }
