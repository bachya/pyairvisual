"""Define package errors."""


class AirVisualError(Exception):
    """Define a base error."""

    pass


class CloudAPIError(AirVisualError):
    """Define an error related to the Cloud API."""

    pass


class NodeProError(AirVisualError):
    """Define an error related to Node/Pro errors."""

    pass


class InvalidKeyError(CloudAPIError):
    """Define an error when the API key is invalid."""

    pass


class KeyExpiredError(CloudAPIError):
    """Define an error when the API key has expired."""

    pass


class LimitReachedError(CloudAPIError):
    """Define an error when the API limit has been reached."""

    pass


class NoStationError(CloudAPIError):
    """Define an error when there's no station for the data requested."""

    pass


class NotFoundError(CloudAPIError):
    """Define an error for when a location (city or node) cannot be found."""

    pass


class RequestError(CloudAPIError):
    """Define an error related to invalid requests."""

    pass


class UnauthorizedError(CloudAPIError):
    """Define an error related to unauthorized requests."""

    pass
