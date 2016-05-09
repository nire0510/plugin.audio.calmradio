import urllib
from xbmcswift2 import Plugin, xbmc, xbmcgui
from api import API


plugin = Plugin()
api = API(plugin)


@plugin.route('/')
def index():
    return plugin.finish([{
        'label': item['name'],
        'icon': item['image'],
        'path': plugin.url_for('show_subcategories', category_id=item['id']),
        'properties': {
            'fanart_image': item['image'],
            'artist_description': item['description']
        }
    } for item in api.get_categories()])


@plugin.route('/category/<category_id>')
def show_subcategories(category_id):
    return plugin.finish([{
        'label': item['name'].capitalize(),
        'icon': item['image'],
        'path': plugin.url_for('show_channels', category_id=category_id, subcategory_id=item['id']),
        'properties': {
            # 'fanart_image': 'special://home/addons/plugin.audio.calmradio/resources/media/fanarts/{0}.jpg'.format(item['id'])
            'fanart_image': item['image']
        }
    } for item in api.get_subcategories(int(category_id))])


@plugin.route('/category/<category_id>/subcategory/<subcategory_id>')
def show_channels(category_id, subcategory_id):
    return plugin.finish([{
        'label': item['title'],
        'icon': item['image'],
        'path': plugin.url_for('play_channel',
                               category_id=category_id,
                               subcategory_id=subcategory_id,
                               channel_id=item['id']),
        'properties': {
            # 'fanart_image': 'special://home/addons/plugin.audio.calmradio/resources/media/fanarts/{0}.jpg'
            #              .format(subcategory_id),
            'fanart_image': item['image'],
            'artist_description': item['description']
        }
    } for item in api.get_channels(int(subcategory_id))])

@plugin.route('/category/<category_id>/subcategory/<subcategory_id>/channel/<channel_id>')
def play_channel(category_id, subcategory_id, channel_id):
    channel = [item for item in api.get_channels(int(subcategory_id))
               if item['id'] == int(channel_id)][0]

    li = xbmcgui.ListItem(channel['title'], channel['description'], channel['image'])
    # li.setArt({'thumb': channel['image'], 'fanart': channel['image']})
    li.setInfo('music', {'Title': channel['title'], 'Artist': channel['description']})
    li.setProperty('mimetype', 'audio/mpeg')
    li.setProperty('IsPlayable', 'true')
    li.setInfo('music', {
        'Title': channel['title'],
        # 'Artist': playlist['slogan'],
        'Artist_Description': channel['description']
    })
    xbmc.Player().play(item=urllib.quote(api.get_url(channel['streams']), safe=':/?='), listitem=li)


if __name__ == '__main__':
    plugin.run(plugin)
