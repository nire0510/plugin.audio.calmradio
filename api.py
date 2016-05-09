from urlparse import urljoin
from bs4 import BeautifulSoup
from cache import Cache
from config import config
import re
import requests
import json


class API(object):
    def __init__(self, plugin):
        self.plugin = plugin

    @staticmethod
    @Cache
    def get_json(url):
        print url
        r = requests.get(url)
        if r.status_code == 200:
            return json.loads(r.text)

    def get_categories(self):
        return [
            {
                'id': 1,
                'name': self.plugin.get_string(32100),
                'image': 'special://home/addons/plugin.audio.calmradio/resources/media/fanarts/0.jpg',
                'description': self.plugin.get_string(32101)
            },
            {
                'id': 3,
                'name': self.plugin.get_string(32102),
                'image': 'special://home/addons/plugin.audio.calmradio/resources/media/fanarts/1.jpg',
                'description': self.plugin.get_string(32103)
            }
        ]

    def get_subcategories(self, category_id):
        return [item['categories'] for item in self.get_json(config['urls']['calm_categories_api'])
                if item['id'] == category_id][0]

    def get_channels(self, subcategory_id):
        return [item['channels'] for item in self.get_json(config['urls']['calm_channels_api'])
                if item['category'] == subcategory_id][0]

    def get_url(self, streams):
        bitrate = {
            '0': '32',
            '1': '64',
            '2': '192',
            '3': '360'
        }[self.plugin.get_setting('bitrate') or 0]

        return streams[bitrate]

    def is_loggedin(self):
        auth = self.plugin.get_storage('auth', TTL=24)
