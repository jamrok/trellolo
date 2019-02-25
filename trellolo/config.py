from ast import literal_eval
from pathlib import Path


class Config:
    config_file = Path("~/.trellolo.cfg").expanduser()

    @classmethod
    def save(cls, api_key: str, token: str):
        """Saves the API key and token to the config file"""
        cls.config_file.write_text(str({"key": api_key, "token": token}))
        return True

    @classmethod
    def load(cls):
        """Loads the API key and token from the config file"""
        cls._api_key = ""
        cls._token = ""
        data = None

        try:
            data = literal_eval(cls.config_file.read_text())
            cls._api_key = data["key"]
            cls._token = data["token"]
        except Exception:
            pass

        return data

    @classmethod
    def api_key(cls):
        """Return the API key"""
        cls.load()
        return cls._api_key

    @classmethod
    def token(cls):
        """Return the token"""
        cls.load()
        return cls._token
