"""Define a base object for interacting with the AirVisual API."""

import requests

import pyairvisual.exceptions

API_BASE_URL = 'http://api.airvisual.com/v2'


class BaseAPI(object):
    """Define a class that represents an API request."""

    def __init__(self, base_url=API_BASE_URL, session=None):
        """Initialize."""
        self.base_url = base_url
        self.session = session

    def request(self, method_type, url, **kwargs):
        """Define a generic request."""
        if self.api_key:
            kwargs.setdefault('params', {})['key'] = self.api_key

        full_url = '{0}/{1}'.format(self.base_url, url)
        method = getattr(self.session
                         if self.session else requests, method_type)
        resp = method(full_url, **kwargs)

        # I don't think it's good form to make end users of pyairvisual have
        # to explicitly catch exceptions from a sub-library, so here, I
        # wrap the Requests HTTPError in my own:
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as exc_info:
            raise pyairvisual.exceptions.HTTPError(str(exc_info))

        return resp

    def get(self, url, **kwargs):
        """Define a generic GET request."""
        return self.request('get', url, **kwargs)
