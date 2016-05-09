from cache import Cache
from config import config
import requests
import json
import time


class User(object):
    def __init__(self, plugin):
        self.plugin = plugin
        self.auth = plugin.get_storage('auth', TTL=24)

    @staticmethod
    def get_json(url):
        r = requests.get(url)
        if r.status_code == 200:
            return json.loads(r.text)

    def is_loggedin(self):
        None

    def authenticate(self, username, password):
        # check if user is already authenticated:

        # authenticate:
        response = self.get_json(config['urls']['calm_auth_host'].format(
            username,
            password
        ))

        # authentication failed:
        if 'error' in response:
            return False

        # authentication succeeded:
        self.auth['auth_timestamp'] = time.time()
        self.auth['auth_token'] = response['token']
        return True