from pytest import fixture,raises
from mock import patch
from gotify_message.gotify_connector import requests
from gotify_message.gotify_connector import GotifyConnector


URL="http://1.2.3.4:8888"
TOKEN="lskd12314sadf1"




@fixture
@patch("requests.get")
def gotify_connector2(m__get):
    m__get().json.return_value = {'health': 'green', 'database': 'green'}
    m__get().ok = True
    yield GotifyConnector(URL, TOKEN)


def mock_get(**kwargs):
    request = requests.Request(**kwargs)
    response = requests.Response()
    response.status_code = 200
    response._content = {'health': 'green', 'database': 'green'}
    return request

@fixture
def gotify_connector():
    with patch("requests.get"):
        requests.get().json.return_value = {'health': 'green', 'database': 'green'}
        requests.get().ok= True
        yield GotifyConnector(URL, TOKEN)

def test_connector(gotify_connector):
    assert gotify_connector.health == "green"
    assert gotify_connector.database == "green"


def test_1():
    with patch("requests.get", new=mock_get):
        requests.get(method="GET")


