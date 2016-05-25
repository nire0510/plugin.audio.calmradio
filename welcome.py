import xbmc, xbmcgui, xbmcplugin
from config import config

ACTION_PREVIOUS_MENU = 10

class WelcomeWindow(xbmcgui.WindowDialog):
    def __init__(self):
        self.setCoordinateResolution(0)

        background = xbmcgui.ControlImage(100, 300, 1720, 500, 'ContentPanel.png')
        self.but1 = xbmcgui.ControlButton(196, 396, 308, 308, '')
        label1 = xbmcgui.ControlImage(200, 400, 300, 300, 'Channels')
        cat1 = xbmcgui.ControlImage(200, 400, 300, 300,
                                    'special://home/addons/plugin.audio.calmradio/resources/media/fanart/1.jpg')
        self.but2 = xbmcgui.ControlButton(596, 396, 308, 308, '')
        cat2 = xbmcgui.ControlImage(600, 400, 300, 300,
                                    'special://home/addons/plugin.audio.calmradio/resources/media/fanart/3.jpg')
        self.but3 = xbmcgui.ControlButton(996, 396, 308, 308, '')
        cat3 = xbmcgui.ControlImage(1000, 400, 300, 300,
                                    'special://home/addons/plugin.audio.calmradio/resources/media/fanart/99.jpg')

        self.addControls((background, self.but1, self.but2, self.but3, cat1, cat2, cat3, label1))

        self.but1.setNavigation(left=self.but3, right=self.but2, up=self.but1, down=self.but1)
        self.but2.setNavigation(left=self.but1, right=self.but3, up=self.but2, down=self.but2)
        self.but3.setNavigation(left=self.but2, right=self.but1, up=self.but3, down=self.but3)

        self.setFocus(self.but1)

    def onAction(self, action):
        if action == ACTION_PREVIOUS_MENU:
            self.close()

    def onControl(self, control):
        if control == self.but1:
            self.setProperty('Category', '1')
            self.close()
        if control == self.but2:
            self.setProperty('Category', '3')
            self.close()
        if control == self.but3:
            self.setProperty('Category', '99')
            self.close()
