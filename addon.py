import sys
import time
import routing
import urllib
from config import config
from api import API
from user import User
from xbmc import executebuiltin, Player, getLocalizedString, log, sleep
from xbmcgui import ListItem, Dialog
from xbmcplugin import addDirectoryItem, endOfDirectory, setContent
from xbmcaddon import Addon
from intro import IntroWindow
from artwork import ArtworkWindow


addon_handle = int(sys.argv[1])
plugin = routing.Plugin()
addon = Addon(config['addon']['id'])
api = API(addon)
artwork = ArtworkWindow()


@plugin.route('/')
def index():
    """
    Main add-on popup
    :return:
    """
    intro_window = IntroWindow(api)
    intro_window.doModal()
    category = intro_window.getProperty('category')
    if category:
        category = int(category)
        sub_category = int(intro_window.getProperty('sub_category'))
        del intro_window

        if category == 1:       # channels
            show_channels(category, sub_category) if category != 99 else show_favorites()
        elif category == 3:     # atmospheres
            show_subcategories(category)
        else:
            show_favorites()    # favorites


@plugin.route('/category/<category_id>')
def show_subcategories(category_id):
    """
    Sub-categories page
    :param category_id: Selected category ID
    :return:
    """
    for item in api.get_subcategories(int(category_id)):
        # list item:
        li = ListItem(item['name'].capitalize(),
            iconImage='{0}/{1}'.format(config['urls']['calm_arts_host'], item['image']),
            thumbnailImage='{0}/{1}'.format(config['urls']['calm_arts_host'], item['image']))
        li.setArt({
            'fanart': '{0}{1}'.format(config['urls']['calm_blurred_arts_host'], item['image'])
        })
        # directory item:
        addDirectoryItem(
            plugin.handle,
            plugin.url_for(show_channels, category_id=category_id, subcategory_id=item['id']),
            li,
            True
        )
    # end of directory:
    endOfDirectory(plugin.handle)


@plugin.route('/category/<category_id>/subcategory/<subcategory_id>')
def show_channels(category_id, subcategory_id):
    """
    Channels page (playable)
    :param category_id: Selected category ID
    :param subcategory_id: Selected sub-category ID
    :return:
    """
    for item in api.get_channels(int(subcategory_id)):
        # list item:
        li = ListItem(u'{0} {1}'.format(item['title'].replace('CALM RADIO -', '').title(),
                                               getLocalizedString(322023) if 'free' not in item['streams'] else '',
                                               item['description']),
            iconImage='{0}/{1}'.format(config['urls']['calm_arts_host'], item['image']),
            thumbnailImage='{0}/{1}'.format(config['urls']['calm_arts_host'], item['image']))
        li.setArt({
            'fanart': '{0}{1}'.format(config['urls']['calm_blurred_arts_host'], item['image'])
        })
        li.addContextMenuItems(
            [(getLocalizedString(32300), 'RunPlugin(plugin://{0}/favorites/add/{1})'
              .format(config['addon']['id'], item['id']))]
        )
        li.setInfo('music', {
            'Title': item['title'].replace('CALM RADIO -', '').title(),
            'Artist_Description': item['description']
        })
        # directory item:
        addDirectoryItem(
            plugin.handle,
            plugin.url_for(play_channel,
                           category_id=category_id,
                           subcategory_id=subcategory_id,
                           channel_id=item['id']),
            li
        )
    # set the content of the directory
    setContent(addon_handle, 'songs')
    # end of directory:
    endOfDirectory(plugin.handle)


@plugin.route('/favorites')
def show_favorites():
    """
    User's favorite channels list
    :return:
    """
    user = User(addon)
    is_authenticated = user.authenticate()

    if is_authenticated:
        favorites = api.get_favorites(user.username, user.token)
        if len(favorites) > 0:
            for item in favorites:
                # list item:
                li = ListItem(u'{0} {1}'.format(item['title'].replace('CALM RADIO -', '').title(),
                                                       '(VIP)' if 'free' not in item['streams'] else '',
                                                       item['description']),
                    iconImage='{0}/{1}'.format(config['urls']['calm_arts_host'], item['image']),
                    thumbnailImage='{0}/{1}'.format(config['urls']['calm_arts_host'], item['image']))
                li.setArt({
                    'fanart': '{0}{1}'.format(config['urls']['calm_blurred_arts_host'], item['image'])
                })
                li.addContextMenuItems(
                    [(getLocalizedString(32301), 'RunPlugin(plugin://{0}/favorites/remove/{1})'
                      .format(config['addon']['id'], item['id']))]
                )
                # directory item:
                addDirectoryItem(
                    plugin.handle,
                    plugin.url_for(play_channel,
                                   category_id=None,
                                   subcategory_id=item['sub_category'],
                                   channel_id=item['id']),
                    li
                )
            # set the content of the directory
            setContent(addon_handle, 'songs')
            # end of directory:
            endOfDirectory(plugin.handle)
        # favorites list is empty:
        else:
            executebuiltin('Notification("{0}", "{1}")'
                           .format(getLocalizedString(30000), getLocalizedString(32306)))
    # user is not authenticated:
    else:
        executebuiltin('Notification("{0}", "{1}")'
                           .format(getLocalizedString(30000), getLocalizedString(32110)))


@plugin.route('/category/<category_id>/subcategory/<subcategory_id>/channel/<channel_id>')
def play_channel(category_id, subcategory_id, channel_id):
    """
    Plays selected song
    :param category_id: Selected category ID
    :param subcategory_id: Selected sub-category ID
    :param channel_id: Selected channel ID
    :return:
    """
    global artwork

    user = User(addon)
    is_authenticated = user.authenticate()
    channel = [item for item in api.get_channels(int(subcategory_id))
               if item['id'] == int(channel_id)][0]
    url = api.get_streaming_url(channel['streams'],
                      user.username,
                      user.token,
                      user.is_authenticated())
    recent_tracks_url = channel['recent_tracks']['vip'] if is_authenticated else channel['recent_tracks']['free']

    # is there a valid URL for channel?
    if url:
        url = urllib.quote(url, safe=':/?=@')
        li = ListItem(channel['title'], channel['description'], channel['image'])
        li.setArt({'thumb': '{0}/{1}'.format(config['urls']['calm_arts_host'], channel['image']),
                   'fanart': '{0}{1}'.format(config['urls']['calm_blurred_arts_host'], channel['image']) })
        li.setInfo('music', {'Title': channel['title'].replace('CALM RADIO -', '').title(), 'Artist': channel['description']})
        li.setProperty('mimetype', 'audio/mpeg')
        li.setProperty('IsPlayable', 'true')
        li.setInfo('music', {
            'Title': channel['title'].replace('CALM RADIO -', '').title(),
            'Artist_Description': channel['description'],
        })
        Player().play(item=url, listitem=li)

        # executebuiltin('AlarmClock(UpdateNowPlaying, "RunPlugin({0})", 00:10, silent, loop)'
        #               .format(plugin.url_for(update_artwork,
        #                                      is_authenticated=is_authenticated,
        #                                      query=recent_tracks_url)))
        artwork.show()
        while(artwork.getProperty('Closed') != 'True'):
            recent_tracks = api.get_json('{0}?{1}'.format(recent_tracks_url, str(int(time.time()))))
            artwork.cover.setImage('{0}/{1}'.format(config['urls']['calm_arts_host'], recent_tracks['now_playing']['album_art']))
            artwork.song.setLabel(recent_tracks['now_playing']['title'])
            artwork.album.setLabel(recent_tracks['now_playing']['album'])
            artwork.artist.setLabel(recent_tracks['now_playing']['artist'])
            sleep(10000)

        log('done!')
        del artwork
        # executebuiltin('CancelAlarm(UpdateNowPlaying, silent)')
    else:
        # members only access
        dialog = Dialog()
        ret = dialog.yesno(getLocalizedString(32200), getLocalizedString(32201))
        if ret == 1:
            addon.openSettings()


@plugin.route('/favorites/add/<channel_id>')
def add_to_favorites(channel_id):
    """
    Adds a channels to user's favorites list
    :param channel_id: Channel ID
    :return:
    """
    user = User(addon)
    is_authenticated = user.authenticate()
    if is_authenticated:
        result = api.add_to_favorites(user.username, user.token, channel_id)
        executebuiltin('Notification("{0}", "{1}"'.format(getLocalizedString(30000),
                                                      getLocalizedString(32302) if result
                                                      else getLocalizedString(32304)))
    else:
        executebuiltin('Notification("{0}", "{1}")'.format(getLocalizedString(30000),
                                                           getLocalizedString(32110)))


@plugin.route('/favorites/remove/<channel_id>')
def remove_from_favorites(channel_id):
    """
    Removes a channels from user's favorites list
    :param channel_id: Channel ID
    :return:
    """
    user = User(addon)
    is_authenticated = user.authenticate()
    if is_authenticated:
        result = api.remove_from_favorites(user.username, user.token, channel_id)
        executebuiltin('Container.Refresh')
        executebuiltin('Notification("{0}", "{1}")'.format(
            getLocalizedString(30000),
            getLocalizedString(32303) if result else getLocalizedString(32305)
        ))
    else:
        executebuiltin('Notification("{0}", "{1}")'.format(
            getLocalizedString(30000),
            getLocalizedString(32110)
        ))

@plugin.route('/update_artwork/<is_authenticated>')
def update_artwork(is_authenticated):
    """
    Updates cnow playing modal info
    :param is_authenticated: Indicates whether user is authenticated or not
    :return:
    """
    global artwork

    recent_tracks = api.get_json(plugin.args['query'][0])
    log('{0}/{1}'.format(config['urls']['calm_arts_host'], recent_tracks['now_playing']['album_art']))
    artwork.update_artwork('{0}/{1}'.format(config['urls']['calm_arts_host'], recent_tracks['now_playing']['album_art']),
                           recent_tracks['now_playing']['album'],
                           recent_tracks['now_playing']['artist'],
                           recent_tracks['now_playing']['title'])
    executebuiltin('Container.Update')

if __name__ == '__main__':
    plugin.run()
    if sys.argv[0] == 'plugin://{0}/'.format(config['addon']['id']) and not addon.getSetting('username'):
        executebuiltin('Notification("{0}", "{1}", 6000, "special://home/addons/{2}/icon.png")'
                       .format(getLocalizedString(30000),
                               getLocalizedString(32202),
                               config['addon']['id']))
