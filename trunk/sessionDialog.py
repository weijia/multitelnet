#Boa:Dialog:sessionDialog

import wx

def create(parent):
    return sessionDialog(parent)

[wxID_SESSIONDIALOG, wxID_SESSIONDIALOGBUTTON1, 
 wxID_SESSIONDIALOGFILEPICKERCTRL1, wxID_SESSIONDIALOGSTATICTEXT1, 
 wxID_SESSIONDIALOGSTATICTEXT2, wxID_SESSIONDIALOGSTATICTEXT3, 
 wxID_SESSIONDIALOGSTATICTEXT4, wxID_SESSIONDIALOGTEXTCTRL1, 
 wxID_SESSIONDIALOGTEXTCTRL2, wxID_SESSIONDIALOGTEXTCTRL3, 
 wxID_SESSIONDIALOGTEXTCTRL4, 
] = [wx.NewId() for _init_ctrls in range(11)]

class sessionDialog(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_SESSIONDIALOG, name=u'sessionDialog',
              parent=prnt, pos=wx.Point(492, 375), size=wx.Size(400, 250),
              style=wx.DEFAULT_DIALOG_STYLE, title='Dialog1')
        self.SetClientSize(wx.Size(392, 223))

        self.textCtrl1 = wx.TextCtrl(id=wxID_SESSIONDIALOGTEXTCTRL1,
              name='textCtrl1', parent=self, pos=wx.Point(88, 64),
              size=wx.Size(176, 21), style=0, value='textCtrl1')

        self.staticText1 = wx.StaticText(id=wxID_SESSIONDIALOGSTATICTEXT1,
              label=u'Server', name='staticText1', parent=self, pos=wx.Point(16,
              72), size=wx.Size(33, 13), style=0)

        self.staticText2 = wx.StaticText(id=wxID_SESSIONDIALOGSTATICTEXT2,
              label=u'port', name='staticText2', parent=self, pos=wx.Point(16,
              104), size=wx.Size(21, 13), style=0)

        self.textCtrl2 = wx.TextCtrl(id=wxID_SESSIONDIALOGTEXTCTRL2,
              name='textCtrl2', parent=self, pos=wx.Point(88, 96),
              size=wx.Size(88, 21), style=0, value='textCtrl2')

        self.staticText3 = wx.StaticText(id=wxID_SESSIONDIALOGSTATICTEXT3,
              label=u'ansiLog', name='staticText3', parent=self,
              pos=wx.Point(16, 128), size=wx.Size(37, 13), style=0)

        self.filePickerCtrl1 = wx.FilePickerCtrl(id=wxID_SESSIONDIALOGFILEPICKERCTRL1,
              message='Select a folder', name='filePickerCtrl1', parent=self,
              path='', pos=wx.Point(232, 128), size=wx.Size(20, 20),
              style=wx.DIRP_DEFAULT_STYLE, wildcard='*.*')

        self.textCtrl3 = wx.TextCtrl(id=wxID_SESSIONDIALOGTEXTCTRL3,
              name='textCtrl3', parent=self, pos=wx.Point(88, 128),
              size=wx.Size(100, 21), style=0, value='textCtrl3')

        self.textCtrl4 = wx.TextCtrl(id=wxID_SESSIONDIALOGTEXTCTRL4,
              name='textCtrl4', parent=self, pos=wx.Point(88, 24),
              size=wx.Size(100, 21), style=0, value='textCtrl4')

        self.staticText4 = wx.StaticText(id=wxID_SESSIONDIALOGSTATICTEXT4,
              label=u'SessionName', name='staticText4', parent=self,
              pos=wx.Point(16, 32), size=wx.Size(64, 13), style=0)

        self.button1 = wx.Button(id=wxID_SESSIONDIALOGBUTTON1, label='button1',
              name='button1', parent=self, pos=wx.Point(304, 184),
              size=wx.Size(75, 23), style=0)
        self.button1.Bind(wx.EVT_BUTTON, self.OnButton1Button,
              id=wxID_SESSIONDIALOGBUTTON1)

    def __init__(self, parent):
        self._init_ctrls(parent)

    def OnButton1Button(self, event):
        self.session = {}
        self.session['sessionName'] = self.textCtrl4.GetValue()
        self.session['server'] = self.textCtrl1.GetValue()
        self.session['port'] = int(self.textCtrl2.GetValue())
        self.session['ansiLog'] = self.textCtrl3.GetValue()
        self.EndModal(True)
        event.Skip()
