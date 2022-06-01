from unittest import TestCase, mock
from gotify_message import GotifyNotification
from gotify_message.gotify_notification import requests


class TestGotifyNotification(TestCase):
    URL = "http://10.0.0.7:8090/message"
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
    def test_notification(self, m__request):
        message = GotifyNotification(
            "http://10.0.0.7:8090",
            "AiOLxxDxYOCc7bY",
            "test_title",
            "test_message", 8
        )
        assert message.url == self.URL
        assert message.headers == self.HEADERS
        assert message.payload == self.PAYLOAD
        assert message.delivered is False

        m__request().ok = True
        message.send()
        requests.post.assert_called_with(
            self.URL,
            headers=self.HEADERS,
            json=self.PAYLOAD
        )
        assert requests.post().ok is True
        assert message.delivered is True

    def test_arguments_number(self):
        with self.assertRaises(TypeError):
            GotifyNotification(12345)


if __name__ == '__main__':
    unittest.main()
