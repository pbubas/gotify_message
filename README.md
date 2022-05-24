# gotify_message

## Description

Python module to push messages to gotify server

Gotify is messaging service that can be installed in LAN network and used without Internet access.

[https://gotify.net/](https://gotify.net/)

## Example use

```python
>>> from gotify_message import GotifyNotification
>>> message=GotifyNotification("http://10.0.0.7:8090", "AiOLxxDxYOCc7bY", "test_title", "test_message")
>>> print(message.json)
{
    "url": "http://10.0.0.7:8090/message",
    "headers": {
        "X-Gotify-Key": "AiOLxxDxYOCc7bY",
        "Content-type": "application/json"
    },
    "payload": {
        "title": "test_title",
        "priority": 5,
        "message": "test_message",
        "extras": {
            "client::display": {
                "contentType": "text/plain"
            }
        }
    }
}
>>> message.send()
<Response [200]>
```
