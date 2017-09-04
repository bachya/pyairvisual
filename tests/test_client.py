"""Define a set of base API tests."""

# pylint: disable=no-self-use,too-few-public-methods,redefined-outer-name
# pylint: disable=wildcard-import,unused-wildcard-import

import json

import requests_mock

import pyairvisual
from tests.fixtures.client import *


def test_client(api_url, response_200):
    """ Tests the creation of a TrashClient from a latitude and longitude """
    with requests_mock.Mocker() as mock:
        mock.get('{}/city'.format(api_url), text=json.dumps(response_200))
        mock.get(
            '{}/nearest_city'.format(api_url), text=json.dumps(response_200))

        client = pyairvisual.Client('abc12345')
        assert client.api_key == 'abc12345'
        assert client.city('City', 'State', 'Country') == response_200
        assert client.nearest_city('fake_lat', 'fake_lon') == response_200
