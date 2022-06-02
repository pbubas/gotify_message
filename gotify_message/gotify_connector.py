
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
    ):

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


class GotifyNotification(GotifyConnector):
    """Basic gotify notification class

    :param url: gotify server url
    :type url: str
    :param token: token to which application send a message
    :type token: str
    :param title: title of the message
    :type title: str
    :param message: message
    :type message: str
    :param priority: message priority, defaults to 5
    :type priority: int, optional
    """
    CONTENT_TYPE = 'plain'

    def __init__(
        self,
        url: str = None,
        token: str = None,
        title: str = None,
        message: str = None,
        priority: int = 5
    ):
        """Constructor method"""

        super().__init__(url, token)

        self.payload = {
            "title": title,
            "priority": priority,
            "message": message,
            "extras": {
                "client::display": {
                     "contentType": "text/"+self.CONTENT_TYPE
                }
            }
        }
        self.delivered = False

    def send(
        self,
        message: str = None,
        title: str = None,
        priority: int = None
    ) -> bool:
        """sends message to gotify server

        :param message: message
        :type message: str
        :param title: title of the message
        :type title: str
        :param priority: message priority, defaults to 5
        :type priority: int, optional
        :return: True is message delivered
        :rtype: bool
        """

        if message:
            self.payload['message'] = message
        if title:
            self.payload['title'] = title
        if priority:
            self.payload['priority'] = priority

        if self._post("/message", self.payload):
            self.delivered = True

        return self.delivered

    @property
    def json(self) -> str:
        """property shows constructed object in string json format`

        :return: constructed object in string json format
        :rtype: str
        """
        return json.dumps(self.__dict__, indent=4)
