import xbmc, xbmcgui

ACTION_PREVIOUS_MENU = 10

class NowPlaying(xbmcgui.WindowDialog):
    def __init__(self):
        background = xbmcgui.ControlImage(40, 40, 270, 154, 'ContentPanel.png')
        self.addControl(background)
        self.strActionInfo = xbmcgui.ControlLabel(100, 400, 200, 200, '', 'font13', '0xFFFF00FF')
        self.addControl(self.strActionInfo)
        self.strActionInfo.setLabel('')
        self.button0 = xbmcgui.ControlButton(42, 42, 270, 30, 'bla')
        self.addControl(self.button0)
        self.button1 = xbmcgui.ControlButton(42, 72, 270, 30, 'bla')
        self.addControl(self.button1)
        self.button2 = xbmcgui.ControlButton(42, 102, 270, 30, 'bla')
        self.addControl(self.button2)
        self.button3 = xbmcgui.ControlButton(42, 132, 270, 30, 'bla')
        self.addControl(self.button3)
        self.button4 = xbmcgui.ControlButton(42, 162, 270, 30, 'bla')
        self.addControl(self.button4)
        self.setFocus(self.button0)
        self.button0.controlDown(self.button1)
        self.button0.controlUp(self.button4)
        self.button1.controlUp(self.button0)
        self.button1.controlDown(self.button2)
        self.button2.controlUp(self.button1)
        self.button2.controlDown(self.button3)
        self.button3.controlUp(self.button2)
        self.button3.controlDown(self.button4)
        self.button4.controlUp(self.button3)
        self.button4.controlDown(self.button0)

    def onAction(self, action):
        if action == ACTION_PREVIOUS_MENU:
            self.close()

    def onControl(self, control):
        if control == self.button0:
            self.close()
        if control == self.button1:
            self.close()
        if control == self.button2:
            self.close()
        if control == self.button3:
            self.close()
        if control == self.button4:
            self.close()