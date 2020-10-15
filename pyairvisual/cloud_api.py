"""Define a client to interact with the AirVisual Cloud API."""
from json.decoder import JSONDecodeError

from aiohttp import ClientSession, ClientTimeout

from .air_quality import AirQuality
from .const import DEFAULT_REQUEST_TIMEOUT
from .errors import raise_on_data_error
from .node import NodeCloudAPI
from .supported import Supported

API_URL_BASE: str = "https://api.airvisual.com/v2"


class CloudAPI:  # pylint: disable=too-few-public-methods
    """Define an object to work with the AirVisual Cloud API."""

    def __init__(self, api_key: str, session: ClientSession = None) -> None:
        """Initialize."""
        self._api_key: str = api_key
        self._session: ClientSession = session

        self.air_quality: AirQuality = AirQuality(self._request)
        self.node: NodeCloudAPI = NodeCloudAPI(self._request)
        self.supported: Supported = Supported(self._request)

    async def _request(
        self, method: str, endpoint: str, *, base_url: str = API_URL_BASE, **kwargs
    ) -> dict:
        """Make a request against the API."""
        kwargs.setdefault("headers", {})
        kwargs["headers"]["Content-Type"] = "application/json"

        kwargs.setdefault("params", {})
        kwargs["params"]["key"] = self._api_key

        use_running_session = self._session and not self._session.closed

        session: ClientSession
        if use_running_session:
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

        raise_on_data_error(data)

        return data
