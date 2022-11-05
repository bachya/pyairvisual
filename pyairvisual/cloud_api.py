"""Define a client to interact with the AirVisual Cloud API."""
from __future__ import annotations

from json.decoder import JSONDecodeError
from typing import Any, cast

from aiohttp import ClientSession, ClientTimeout

from .air_quality import AirQuality
from .const import LOGGER
from .errors import AirVisualError
from .node import NodeCloudAPI
from .supported import Supported

API_URL_BASE = "https://api.airvisual.com/v2"

DEFAULT_REQUEST_TIMEOUT = 10


class CloudAPIError(AirVisualError):
    """Define an error related to the Cloud API."""

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


ERROR_CODES: dict[str, type[AirVisualError]] = {
    "api_key_expired": KeyExpiredError,
    "call_limit_reached": LimitReachedError,
    "city_not_found": NotFoundError,
    "feature_not_available": UnauthorizedError,
    "forbidden": UnauthorizedError,
    "incorrect_api_key": InvalidKeyError,
    "no_nearest_station": NoStationError,
    "node not found": NotFoundError,
    "payment required": InvalidKeyError,
    "permission_denied": UnauthorizedError,
    "too_many_requests": LimitReachedError,
}


def raise_on_data_error(data: dict[str, Any]) -> None:
    """Raise an error if the data payload suggests there is one.

    Args:
        data: A response data payload from the API.

    Raises:
        error: An appropriate API error (a subclass of AirVisualError).
    """
    if "data" not in data or data.get("status") == "success":
        return

    try:
        [error] = [
            v for k, v in ERROR_CODES.items() if k in data["data"]["message"].lower()
        ]
    except ValueError:
        error = AirVisualError
    raise error(data)


class CloudAPI:  # pylint: disable=too-few-public-methods
    """Define an object to work with the AirVisual Cloud API."""

    def __init__(self, api_key: str, session: ClientSession | None = None) -> None:
        """Initialize.

        Args:
            api_key: An API key.
            session: An optional aiohttp ClientSession.
        """
        self._api_key = api_key
        self._session: ClientSession | None = session

        self.air_quality = AirQuality(self._request)
        self.node = NodeCloudAPI(self._request)
        self.supported = Supported(self._request)

    async def _request(
        self,
        method: str,
        endpoint: str,
        *,
        base_url: str = API_URL_BASE,
        **kwargs: dict[str, Any],
    ) -> dict[str, Any]:
        """Make a request against the API.

        Args:
            method: An HTTP method.
            endpoint: A relative API endpoint to query.
            base_url: The base API URL to use.
            **kwargs: Extra arguments to send with the API request.

        Returns:
            An API response payload.
        """
        kwargs.setdefault("headers", {})
        kwargs["headers"]["Content-Type"] = "application/json"

        kwargs.setdefault("params", {})
        kwargs["params"]["key"] = self._api_key

        if use_running_session := self._session and not self._session.closed:
            session = self._session
        else:
            session = ClientSession(
                timeout=ClientTimeout(total=DEFAULT_REQUEST_TIMEOUT)
            )

        try:
            async with session.request(
                method, f"{base_url}/{endpoint}", **kwargs
            ) as resp:
                data = await resp.json(content_type=None)
        except JSONDecodeError:
            # The response can't be parsed as JSON, so we'll use its body text
            # in an error:
            response_text = await resp.text()
            data = {"status": "fail", "data": {"message": response_text}}
        finally:
            if not use_running_session:
                await session.close()

        if isinstance(data, str):
            # In some cases, the AirVisual API will return a quoted string in its
            # response body (e.g., "\"node not found\""), which is technically valid
            # JSON. Additionally, AirVisual sets that response's Content-Type header
            # to application/json (#smh). Together, these factors will allow a
            # non-true-JSON  payload to escape the try/except above. So, if we get
            # here, we use the string value (with quotes removed) to raise an error:
            response_text = data.replace('"', "")
            data = {"status": "fail", "data": {"message": response_text}}

        LOGGER.debug("Data received for /%s: %s", endpoint, data)

        raise_on_data_error(data)

        return cast(dict[str, Any], data)
