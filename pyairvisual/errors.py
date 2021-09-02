"""Define package errors."""


class AirVisualError(Exception):
    """Define a base error."""

    pass


class InvalidKeyError(AirVisualError):
    """Define an error when the API key is invalid."""

    pass


class KeyExpiredError(AirVisualError):
    """Define an error when the API key has expired."""

    pass


class LimitReachedError(AirVisualError):
    """Define an error when the API limit has been reached."""

    pass


class NoStationError(AirVisualError):
    """Define an error when there's no station for the data requested."""

    pass


class NodeProError(AirVisualError):
    """Define an error related to Node/Pro errors."""

    pass


class NotFoundError(AirVisualError):
    """Define an error for when a location (city or node) cannot be found."""

    pass


class RequestError(AirVisualError):
    """Define an error related to invalid requests."""

    pass


class UnauthorizedError(AirVisualError):
    """Define an error related to unauthorized requests."""

    pass
