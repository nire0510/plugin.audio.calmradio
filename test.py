# -*- coding: utf-8 -*-
from api import API
from xbmcswift2 import Plugin
from user import User
from config import config
import urllib


plugin = Plugin()
user = User(plugin)
api = API(plugin)

# for category in api.get_categories():
#     print category['label']

# for sub_category in api.get_all_subcategories():
#     print sub_category['name']

# for sub_category in api.get_subcategories(1):
#     print sub_category['name']

# for channel in api.get_channels(7):
#     print channel['id'], channel['streams']['free']

# print api.add_to_favorites('username', 'password', 9)
# print api.remove_from_favorites('username', 'password', 9)

# for channel in api.get_favorites('username', 'password'):
#     print channel['id']


# print user.authenticate()
# print user.check_sua()

# for channel in api.get_all_subcategories():
#     urllib.urlretrieve('{0}{1}'.format(config['urls']['calm_arts_host'], channel['image']),
#                        'resources/media/fanart/subcategory-{0}.jpg'.format(channel['id']))

# for channel in api.get_all_channels():
#     urllib.urlretrieve('{0}{1}'.format(config['urls']['calm_arts_host'], channel['image']),
#                        'resources/media/fanart/channel-{0}.jpg'.format(channel['id']))

# for f in resources/media/fanart/subcategory-*; do convert $f -resize 1200x800\! $f; done
# for f in resources/media/fanart/subcategory-*; do convert $f -blur 0x40 $f; done

# for f in resources/media/fanart/channel-*; do convert $f -resize 1200x800\! $f; done
# for f in resources/media/fanart/channel-*; do convert $f -blur 0x40 $f; done