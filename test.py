# -*- coding: utf-8 -*-
from api import API
from xbmcswift2 import Plugin
from user import User


plugin = Plugin()
user = User(plugin)
api = API(plugin)

# for category in api.get_categories():
#     print category['label']

# for sub_category in api.get_subcategories(1):
#     print sub_category['name']

# for channel in api.get_channels(9):
#     print channel['id']

user.authenticate('nir', 'nirocalm123')