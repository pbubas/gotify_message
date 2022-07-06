import unittest
import pytest
from unittest import mock
from gotify_message.gotify_connector import requests
from gotify_message.gotify_connector import GotifyConnector

URL = "http://10.0.0.7:8090"
TOKEN = "tokenASDASDA"


@pytest.fixture
def url():
    return URL

@pytest.fixture
def token():
    return TOKEN

@pytest.fixture
def health_response():
    return {'health': 'green', 'database': 'green'}

def mock_response(fail = None):
    def request(method, **kwargs):
        response = requests.Response()
        request = requests.Request(method)
        response.status_code = 200
        for attr in kwargs:
            if hasattr(request, attr):
                setattr(request, attr, kwargs[attr])
        response.request = request
        if fail:
            response._content = b'{"health":"red","database":"red"}'
        else:
            response._content = b'{"health":"green","database":"green"}'
        return response
    return request


@pytest.fixture
def gotify_connector(url, token, health_response):
    with mock.patch("requests.get", new=mock.MagicMock()):
        requests.get().json.return_value = health_response
        requests.get().ok = True
        yield GotifyConnector(url, token)

@pytest.fixture
def gotify_connector_mock_response(url, token):
    with mock.patch("requests.get", new=mock_response()):
        yield GotifyConnector(url, token)

@pytest.fixture
def gotify_connector_mock_response_fail(url, token):
    with mock.patch("requests.get", side_effect=mock_response(fail=True)):
        yield GotifyConnector(url, token)

class TestConnector:
    
    def test_constructor(self, gotify_connector):
        assert gotify_connector.url == "http://10.0.0.7:8090"
        assert gotify_connector.token == "tokenASDASDA"
        assert gotify_connector.health == "green"
        assert gotify_connector.database == "green"

    def test_constructor_2(self):
        with mock.patch("requests.get"):
            requests.get().json.return_value = {'health': 'green', 'database': 'green'}
            requests.get().ok = True
            gotify_connector = GotifyConnector("http://10.0.0.7:8090","tokenASDASDA")       
            assert gotify_connector.url == "http://10.0.0.7:8090"
            assert gotify_connector.token == "tokenASDASDA"
            assert gotify_connector.health == "green"
            assert gotify_connector.database == "green"

    def test_constructor_3(self):
        with mock.patch("requests.get"):
            requests.get.side_effect = requests.exceptions.HTTPError
            with pytest.raises(requests.exceptions.HTTPError):
               gotify_connector = GotifyConnector("http://10.0.0.7:8090","tokenASDASDA")


    def test_constructor_mock_response(self, gotify_connector_mock_response):
        assert gotify_connector_mock_response.url == "http://10.0.0.7:8090"
        assert gotify_connector_mock_response.token == "tokenASDASDA"
        assert gotify_connector_mock_response.health == "green"
        assert gotify_connector_mock_response.database == "green"

    def test_constructor_mock_response_fail(self, gotify_connector_mock_response_fail):
        assert gotify_connector_mock_response_fail.url == "http://10.0.0.7:8090"
        assert gotify_connector_mock_response_fail.token == "tokenASDASDA"
        assert gotify_connector_mock_response_fail.health == "red"
        assert gotify_connector_mock_response_fail.database == "red"

    @mock.patch("requests.get", side_effect=mock_response(fail=True))
    def test_constructor_1(self, m__get):
        client = GotifyConnector("http://10.0.0.7:8090", "daskjdsakjn")
        assert client.url == "http://10.0.0.7:8090"
        assert client.token == "daskjdsakjn"
        assert client.health == "red"
        assert client.database == "red"



