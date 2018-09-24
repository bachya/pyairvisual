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


class NotFoundError(AirVisualError):
    """Define an error for when a city cannot be found."""

    pass


class RequestError(AirVisualError):
    """Define an error related to invalid requests."""

    pass


class UnauthorizedError(AirVisualError):
    """Define an error related to unauthorized requests."""

    pass


ERROR_CODES = {
    'api_key_expired': KeyExpiredError,
    'call_limit_reached': LimitReachedError,
    'city_not_found': NotFoundError,
    'incorrect_api_key': InvalidKeyError,
    'no_nearest_station': NoStationError,
    'permission_denied': UnauthorizedError,
}


def raise_error(error_type: str) -> None:
    """Raise the appropriate error based on error message."""
    try:
        [error] = [v for k, v in ERROR_CODES.items() if k in error_type]
    except ValueError:
        error = AirVisualError
    raise error(error_type)
