"""Define an AirVisual client."""

import pyairvisual.api as api


class Client(api.BaseAPI):
    """Define an AirVisual API client."""

    def __init__(self, api_key):
        """Initialize."""
        self._api_key = api_key
        super(Client, self).__init__()

    @property
    def api_key(self):
        """Define a property for the AirVisual API key."""
        return self._api_key

    def city(self, city, state, country):
        """Retrieve pollution data for specific city."""
        return self.get(
            'city', params={'city': city,
                            'state': state,
                            'country': country}).json()

    def nearest_city(self, latitude, longitude, radius=1000):
        """Retrieve pollution data for city nearest to a lat/long/radius."""
        return self.get(
            'nearest_city',
            params={'lat': latitude,
                    'lon': longitude,
                    'rad': radius}).json()
