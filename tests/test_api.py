"""Define a set of base API tests."""

# pylint: disable=no-self-use,too-few-public-methods,redefined-outer-name
# pylint: disable=wildcard-import,unused-wildcard-import

import pytest
import requests_mock

import pyairvisual
from tests.fixtures.client import *


def test_api(api_url):
    """ Tests the creation of a TrashClient from a latitude and longitude """

    with requests_mock.Mocker() as mock:
        mock.get('{}/city'.format(api_url), status_code=404)

        with pytest.raises(pyairvisual.exceptions.HTTPError) as exc_info:
            client = pyairvisual.Client('abc12345')
            client.city('Fake City', 'Fake State', 'Fake Country')
            assert '404' in str(exc_info)
