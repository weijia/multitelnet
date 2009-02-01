#Boa:Frame:playBackFrame

import wx

def create(parent):
    return playBackFrame(parent)

[wxID_PLAYBACKFRAME, wxID_PLAYBACKFRAMEDEBUG, wxID_PLAYBACKFRAMESTEPBUTTON, 
 wxID_PLAYBACKFRAMETEXTCTRL1, 
] = [wx.NewId() for _init_ctrls in range(4)]

class playBackFrame(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_PLAYBACKFRAME, name=u'playBackFrame',
              parent=prnt, pos=wx.Point(535, 326), size=wx.Size(400, 250),
              style=wx.DEFAULT_FRAME_STYLE, title=u'playbackControl')
        self.SetClientSize(wx.Size(392, 223))

        self.stepButton = wx.Button(id=wxID_PLAYBACKFRAMESTEPBUTTON,
              label=u'step', name=u'stepButton', parent=self, pos=wx.Point(160,
              8), size=wx.Size(224, 96), style=0)
        self.stepButton.Bind(wx.EVT_BUTTON, self.OnStepButtonButton,
              id=wxID_PLAYBACKFRAMESTEPBUTTON)

        self.textCtrl1 = wx.TextCtrl(id=wxID_PLAYBACKFRAMETEXTCTRL1,
              name='textCtrl1', parent=self, pos=wx.Point(24, 16),
              size=wx.Size(108, 37), style=0, value=u'10')

        self.debug = wx.Button(id=wxID_PLAYBACKFRAMEDEBUG,
              label=u'debug switcher', name=u'debug', parent=self,
              pos=wx.Point(240, 152), size=wx.Size(99, 23), style=0)
        self.debug.Bind(wx.EVT_BUTTON, self.OnDebugButton,
              id=wxID_PLAYBACKFRAMEDEBUG)

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.view = None

    def OnStepButtonButton(self, event):
        self.view.step(int(self.textCtrl1.GetValue()))
        event.Skip()

    def OnDebugButton(self, event):
        self.view.switchDebug()
        #event.Skip()


class dummyConnection:
    def loseConnection(self):
        pass
    def writeKey(self,key):
        pass
    def write(self, key):
        pass
    def sendWindowSize(self):
        pass
    def writeCtrlKey(self, key):
        pass
