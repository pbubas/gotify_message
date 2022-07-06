from unittest import TestCase, mock
from gotify_message import GotifyNotification
from gotify_message.gotify_connector import GotifyConnector
from gotify_message.gotify_connector import requests


class TestGotifyNotification(TestCase):
    URL = "http://10.0.0.7:8090"
    RESOURCE = "/message"
    HEADERS = {
        "X-Gotify-Key": "AiOLxxDxYOCc7bY",
        "Content-type": 'application/json'
    }
    PAYLOAD = {
        "title": "test_title",
        "priority": 8,
        "message": "test_message",
        "extras": {
            "client::display": {
                    "contentType": "text/plain"
            }
        }
    }

    @mock.patch("requests.post")
    @mock.patch("requests.get")
    def test_notification(self, m__post, m__get):

        m__get().ok = True
        m__get().json.return_value  = {'health': 'green', 'database': 'green'}

        m__post().ok = True
        m__post().json.return_value  = {'health': 'green', 'database': 'green'}


        message = GotifyNotification(
            "http://10.0.0.7:8090",
            "AiOLxxDxYOCc7bY",
            "test_title",
            "test_message", 8
        )
        assert message.url == self.URL
        assert message.payload == self.PAYLOAD
        assert message.delivered is False


        message.send()
        requests.post.assert_called_with(
            self.URL + self.RESOURCE,
            headers=self.HEADERS,
            json=self.PAYLOAD
        )
        assert requests.post().ok is True
        assert message.delivered is True

    def test_arguments_number(self):
        with self.assertRaises(TypeError):
            GotifyNotification(12345)


class TestGotifyConnector(TestCase):

    @mock.patch("requests.get")
    def test_constructor(self, m__get):
        m__get().ok = True
        m__get().json.return_value  = {'health': 'green', 'database': 'green'}
        client = GotifyConnector("http://1.1.1.1:8888", "tokenASDASDA")
        assert client.token == "tokenASDASDA"


if __name__ == '__main__':
    unittest.main()
