import json
import requests


class JsonConfig(object):
    @classmethod
    def load(self, filename) -> dict:
        try:
            with open(filename, 'r') as file:
                return json.load(file)
        except Exception as ex:
            print("Unable to load configuration from file {0}".format(filename))
            raise

    @classmethod
    def load_from_url(self, url) -> dict:
        try:
            return requests.get(url).json()
        except Exception as ex:
            print("Unable to load config from URL {0}".format(url))
            raise