from urlparse import urljoin
from bs4 import BeautifulSoup
from cache import Cache
from config import config
import re
import requests
import xml.etree.ElementTree as ET


class API(object):
    def __init__(self, plugin):
        self.plugin = plugin

    @staticmethod
    @Cache
    def get_calm_data():
        r = requests.get(config['urls']['calm_api'])
        if r.status_code == 200:
            return ET.fromstring(r.content)

    def get_categories(self):
        return [
            {
                'id': '0',
                'label': self.plugin.get_string(32100),
                'icon': 'special://home/addons/plugin.audio.calmradio/resources/media/fanarts/0.jpg',
                'description': self.plugin.get_string(32101)
            },
            {
                'id': '1',
                'label': self.plugin.get_string(32102),
                'icon': 'special://home/addons/plugin.audio.calmradio/resources/media/fanarts/1.jpg',
                'description': self.plugin.get_string(32103)
            }
        ]

    def get_subcategories(self):
        return [
            {
                'id': '0.1',
                'label': self.plugin.get_string(32104),
                'icon': ''
            },
            {
                'id': '0.2',
                'label': self.plugin.get_string(32105),
                'icon': ''
            },
            {
                'id': '0.3',
                'label': self.plugin.get_string(32106),
                'icon': ''
            },
            {
                'id': '0.4',
                'label': self.plugin.get_string(32107),
                'icon': ''
            },
            {
                'id': '0.5',
                'label': self.plugin.get_string(32108),
                'icon': ''
            },
            {
                'id': '0.6',
                'label': self.plugin.get_string(32109),
                'icon': ''
            },
            {
                'id': '0.7',
                'label': self.plugin.get_string(32110),
                'icon': ''
            },
            {
                'id': '0.8',
                'label': self.plugin.get_string(32111),
                'icon': ''
            },
            {
                'id': '0.9',
                'label': self.plugin.get_string(32112),
                'icon': ''
            },
            {
                'id': '1.0',
                'label': self.plugin.get_string(32113),
                'icon': ''
            },
            {
                'id': '1.1',
                'label': self.plugin.get_string(32114),
                'icon': ''
            },
            {
                'id': '1.2',
                'label': self.plugin.get_string(32115),
                'icon': ''
            },
            {
                'id': '1.3',
                'label': self.plugin.get_string(32116),
                'icon': ''
            },
            {
                'id': '1.4',
                'label': self.plugin.get_string(32117),
                'icon': ''
            }
        ]

    def get_channels(self, subcategory_id):
        items = []
        root = API.get_calm_data()
        for item in root.findall('item'):
            if item.find('category').text == subcategory_id and item.find('active').text == 'true':
                items.append(
                    {
                        'label': item.find('title').text,
                        'visual': urljoin(config['urls']['calm_website'], item.find('visual').text),
                        'description': item.find('description').text,
                        'url': self.get_url(item)
                    }
                )
        return items

    def get_url(self, item):
        bitrate = {
            '0': '0',
            '1': '64',
            '2': '128',
            '3': '192'
        }[self.plugin.get_setting('bitrate') or 0]

        for file in item.findall('file'):
            url = file.attrib['src']
            if file.attrib['bitrate'] == bitrate:
                break

        if self.plugin.get_setting('username') and self.plugin.get_setting('password'):
            url = url.replace('http://','http://{0}:{1}@'
                           .format(self.plugin.get_setting('username'),
                                   self.plugin.get_setting('password')))

        return url
