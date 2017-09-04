"""
File: client.py
Author: Aaron Bach
Email: bachya1208@gmail.com
Github: https://github.com/bachya/pyairvisual
"""

# -*- coding: utf-8 -*-
# pylint: disable=redefined-outer-name

import pytest


@pytest.fixture(scope='session')
def api_url():
    """Define an API url fixture."""
    return 'http://api.airvisual.com/v2'


@pytest.fixture(scope='session')
def response_200():
    """Define a successful response."""
    return {
        "status": "success",
        "data": {
            "city": "Denver",
            "state": "Colorado",
            "country": "USA",
            "location": {
                "type": "Point",
                "coordinates": [-105.00523, 39.7794]
            },
            "current": {
                "weather": {
                    "ts": "2017-09-04T10:00:00.000Z",
                    "tp": 16,
                    "pr": 1026,
                    "hu": 41,
                    "ws": 2,
                    "wd": 200,
                    "ic": "50n"
                },
                "pollution": {
                    "ts": "2017-09-04T09:00:00.000Z",
                    "aqius": 146,
                    "mainus": "p2",
                    "aqicn": 73,
                    "maincn": "p2"
                }
            }
        }
    }
