import json
from .gotify_connector import GotifyConnector


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
