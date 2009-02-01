#Boa:MDIChild:rtfConnectionChildFrame

import wx
import wx.richtext

def create(parent):
    return rtfConnectionChildFrame(parent)

[wxID_RTFCONNECTIONCHILDFRAME, wxID_RTFCONNECTIONCHILDFRAMERICHTEXTCTRL1, 
] = [wx.NewId() for _init_ctrls in range(2)]

class rtfConnectionChildFrame(wx.MDIChildFrame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.MDIChildFrame.__init__(self, id=wxID_RTFCONNECTIONCHILDFRAME,
              name=u'rtfConnectionChildFrame', parent=prnt, pos=wx.Point(508,
              236), size=wx.Size(400, 250), style=wx.DEFAULT_FRAME_STYLE,
              title='MDIChildFrame1')
        self.SetClientSize(wx.Size(392, 223))

        self.richTextCtrl1 = wx.richtext.RichTextCtrl(id=wxID_RTFCONNECTIONCHILDFRAMERICHTEXTCTRL1,
              parent=self, pos=wx.Point(0, 0), size=wx.Size(392, 223),
              style=wx.richtext.RE_MULTILINE, value=u'richTextCtrl1\n')
        self.richTextCtrl1.SetAutoLayout(True)
        self.richTextCtrl1.SetLabel(u'text')
        self.richTextCtrl1.Bind(wx.EVT_KEY_DOWN, self.OnRichTextCtrl1KeyDown)
        self.richTextCtrl1.Bind(wx.EVT_CHAR, self.OnRichTextCtrl1Char)

    def __init__(self, parent):
        self._init_ctrls(parent)

    def connect(self, session):
        from rtfCtrlAdapter import rtfTextAdapter
        self.adapter = rtfTextAdapter(self.richTextCtrl1)
        from telnetConnector import connectTelnet
        connectTelnet(session, self.adapter)

    def OnRichTextCtrl1KeyDown(self, event):
        self.adapter.keyDown(event)


    def OnRichTextCtrl1Char(self, event):
        self.adapter.char(event)

