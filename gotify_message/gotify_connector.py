import logging
import requests
import json

LOG = logging.getLogger(__name__)


class GotifyConnector:
    URL = None
    TOKEN = None

    def __init__(
        self,
        url: str = None,
        token: str = None
    ):

        self.url = (url or self.URL)
        self.token = (token or self.TOKEN)
        self._check_status()

    def _get(self, resource, timeout: int = None) -> dict:
        headers = {"X-Gotify-Key": self.token}
        url = self.url + resource
        response = requests.get(url, headers=headers, timeout=timeout)

        if response.ok:
            return response.json()
        else:
            error = (
                f"'{url}' response error:\n" +
                json.dumps(response.json(), indent=3)
            )
            LOG.error(error)
            return None

    def _post(
        self,
        resource: dict = None,
        payload: dict = None,
        headers: dict = None,
    ) --> dict:

        _headers = {
            "X-Gotify-Key": self.token,
            "Content-type": "application/json"
        }
        if headers:
            _headers |= headers
        url = self.url + resource
        response = requests.post(url, headers=_headers, json=payload)

        if response.ok:
            return response.json()
        else:
            error = (
                f"'{url}' response error:\n" +
                json.dumps(response.json(), indent=3)
            )
            LOG.error(error)
            return None

    @property
    def health(self) -> str:
        response = self._get("/health", timeout=10)
        status = response.get("health")
        return status

    @property
    def database(self) -> str:
        response = self._get("/health", timeout=10)
        status = response.get("database")
        return status

    def _check_status(self):
        if self.health != "green":
            log_msg = (
                f"Gotify service {self.url} health probblem: {self.health}"
            )
            LOG.warning(log_msg)
        else:
            log_msg = (
                f"Gotify service {self.url} health status: {self.health}"
            )
            LOG.debug(log_msg)

        if self.database != "green":
            log_msg = (
                f"Gotify service {self.url} database probblem: {self.database}"
            )
            LOG.warning(log_msg)
        else:
            log_msg = (
                f"Gotify service {self.url} database status: {self.database}"
            )
            LOG.debug(log_msg)
