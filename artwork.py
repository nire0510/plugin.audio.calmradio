import xbmc, xbmcgui, xbmcplugin
from config import config

ACTION_PARENT_DIR = 9
ACTION_PREVIOUS_MENU = 10

class ArtworkWindow(xbmcgui.WindowDialog):
    def __init__(self):
        self.setCoordinateResolution(0) # 1920x1080
        dimentions = {
            'spacing': {
              'normal': 20,
              'medium': 15,
              'small': 10
            },
            'cover': {
                'x1': 560,
                'x2': 1360,
                'y1': 140,
                'y2': 940,
            },
            'details': {
                'height': 160
            },
            'label': {
                'height': 30
            }
        }

        # overlay
        overlay = xbmcgui.ControlImage(0,
                                       0,
                                       1920,
                                       1080,
                                       'special://home/addons/plugin.audio.calmradio/resources/media/000000-0.8.png')

        # album art
        self.cover = xbmcgui.ControlImage(
            dimentions['cover']['x1'],
            dimentions['cover']['y1'] - dimentions['details']['height'] / 2,
            dimentions['cover']['x2'] - dimentions['cover']['x1'],
            dimentions['cover']['y2'] - dimentions['cover']['y1'],
            'http://arts.calmradio.com/31a3c5d5-3f8f-4a38-9531-9faf0cfe4c71.jpg'
        )

        # details
        details = xbmcgui.ControlImage(dimentions['cover']['x1'],
                                     dimentions['cover']['y2'] - dimentions['details']['height'] / 2,
                                     dimentions['cover']['x2'] - dimentions['cover']['x1'],
                                     dimentions['details']['height'],
                                     'special://home/addons/plugin.audio.calmradio/resources/media/18B0E2-1.png')

        # logo
        logo = xbmcgui.ControlImage(dimentions['cover']['x1'] + dimentions['spacing']['normal'],
                                    dimentions['cover']['y2'] + dimentions['spacing']['normal']
                                     - dimentions['details']['height'] / 2,
                                    dimentions['details']['height'] - 2 * dimentions['spacing']['normal'],
                                    dimentions['details']['height'] - 2 * dimentions['spacing']['normal'],
                                    'special://home/addons/plugin.audio.calmradio/icon.png')


        # song name
        self.song = xbmcgui.ControlLabel(
            dimentions['cover']['x1'] + dimentions['spacing']['normal'] +
                dimentions['details']['height'] - 2 * dimentions['spacing']['normal'] +
                dimentions['spacing']['normal'],
            dimentions['cover']['y2'] + dimentions['spacing']['normal'] -
                dimentions['details']['height'] / 2,
            dimentions['cover']['x2'] - dimentions['cover']['x1'],
            dimentions['label']['height'],
            'Song Name'
        )

        # album title
        self.album = xbmcgui.ControlLabel(
            dimentions['cover']['x1'] + dimentions['spacing']['normal'] +
                dimentions['details']['height'] - 2 * dimentions['spacing']['normal'] +
                dimentions['spacing']['normal'],
            dimentions['cover']['y2'] + 2 * dimentions['spacing']['normal'] -
                dimentions['details']['height'] / 2 +
                dimentions['label']['height'],
            dimentions['cover']['x2'] - dimentions['cover']['x1'],
            dimentions['label']['height'],
            'Album Title',
            font='font12'
        )

        # artist
        self.artist = xbmcgui.ControlLabel(
            dimentions['cover']['x1'] + dimentions['spacing']['normal'] +
                dimentions['details']['height'] - 2 * dimentions['spacing']['normal'] +
                dimentions['spacing']['normal'],
            dimentions['cover']['y2'] + 2 * dimentions['spacing']['normal'] -
                dimentions['details']['height'] / 2 +
                2 * dimentions['label']['height'],
            dimentions['cover']['x2'] - dimentions['cover']['x1'],
            dimentions['label']['height'],
            'Artist Name',
            font='font12'
        )


        self.addControls((overlay, self.cover, details, logo,
                          self.song, self.album, self.artist))


    def onAction(self, action):
        if action == ACTION_PREVIOUS_MENU or action == ACTION_PARENT_DIR:
            # xbmc.executebuiltin('CancelAlarm(GetNowPlaying, silent)')
            self.setProperty('Closed', 'True')
            self.close()

    def update_artwork(self, cover, album_title, artist, song):
        self.album.setLabel(album_title)
        self.cover.setImage(cover)
        # xbmc.executebuiltin('Container.Refresh')
