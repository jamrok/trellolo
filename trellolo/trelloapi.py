import requests


class TrelloAPI:

    api_key = None
    token = None
    base_url = "https://api.trello.com"
    url = None
    initialized = False

    @classmethod
    def __init__(cls, key="", token="", url=""):
        cls.url = cls.base_url + url
        if key and token and cls.valid_credentials(key, token):
            cls.api_key = key
            cls.token = token

    @classmethod
    def send_request(
        cls, url="", method="GET", headers={}, params={}, data={},
        key="", token=""
    ):
        """Make a generic Trello API call."""

        headers["Accept"] = "application/json"
        # Add the API Key and token to the query string
        if not key:
            key = cls.api_key
        if not token:
            token = cls.token
        params.update({"key": key, "token": token})

        # Combine args
        kwargs = {
            "method": method.upper(),
            "url": cls.url + url,
            "headers": headers,
            "params": params,
            "data": data,
        }

        resp = requests.request(**kwargs)
        if resp.status_code == 200:
            return resp.json()
        else:
            raise requests.HTTPError(f"{resp.status_code}: {resp.text}")

    @classmethod
    def valid_credentials(cls, key, token):
        """Validate the API key"""
        cls.send_request(url=f"/1/tokens/{token}", key=key, token=token)
        cls.initialized = True
        return True
