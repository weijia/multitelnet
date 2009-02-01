#Boa:Dialog:chooseScript

import wx
from configUtil import *

def create(parent):
    return chooseScript(parent)

[wxID_CHOOSESCRIPT, wxID_CHOOSESCRIPTBROWSERBUT, wxID_CHOOSESCRIPTOKBUT, 
 wxID_CHOOSESCRIPTPROMPTSTRING, wxID_CHOOSESCRIPTSCRIPTPATH, 
 wxID_CHOOSESCRIPTSCRIPTPATHLIST, wxID_CHOOSESCRIPTTIMEOUTSETTING, 
] = [wx.NewId() for _init_ctrls in range(7)]

class chooseScript(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_CHOOSESCRIPT, name=u'chooseScript',
              parent=prnt, pos=wx.Point(518, 379), size=wx.Size(327, 250),
              style=wx.DEFAULT_DIALOG_STYLE,
              title=u'Please choose a script file')
        self.SetClientSize(wx.Size(319, 223))

        self.okBut = wx.Button(id=wxID_CHOOSESCRIPTOKBUT, label=u'OK',
              name=u'okBut', parent=self, pos=wx.Point(216, 176),
              size=wx.Size(75, 23), style=0)
        self.okBut.Bind(wx.EVT_BUTTON, self.OnOkButButton,
              id=wxID_CHOOSESCRIPTOKBUT)

        self.scriptPath = wx.ComboBox(choices=[],
              id=wxID_CHOOSESCRIPTSCRIPTPATH, name=u'scriptPath', parent=self,
              pos=wx.Point(40, 24), size=wx.Size(162, 21), style=0,
              value='comboBox1')

        self.browserBut = wx.Button(id=wxID_CHOOSESCRIPTBROWSERBUT,
              label=u'Browser', name=u'browserBut', parent=self,
              pos=wx.Point(216, 24), size=wx.Size(75, 23), style=0)
        self.browserBut.Bind(wx.EVT_BUTTON, self.OnBrowserButButton,
              id=wxID_CHOOSESCRIPTBROWSERBUT)

        self.promptString = wx.ComboBox(choices=[],
              id=wxID_CHOOSESCRIPTPROMPTSTRING, name=u'promptString',
              parent=self, pos=wx.Point(40, 144), size=wx.Size(130, 21),
              style=0, value='comboBox2')

        self.timeoutSetting = wx.SpinCtrl(id=wxID_CHOOSESCRIPTTIMEOUTSETTING,
              initial=5, max=100, min=0, name=u'timeoutSetting', parent=self,
              pos=wx.Point(40, 176), size=wx.Size(117, 21),
              style=wx.SP_ARROW_KEYS)

        self.scriptPathList = wx.ListBox(choices=[],
              id=wxID_CHOOSESCRIPTSCRIPTPATHLIST, name=u'scriptPathList',
              parent=self, pos=wx.Point(40, 64), size=wx.Size(160, 63),
              style=0)

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.path = False
        self.pathSelected = False
    
    def initHist(self, config):
        try:
            self.hist = config['histScirptPath']
        except KeyError:
            config['histScirptPath'] = []
            self.hist = config['histScirptPath']
        #self.histScriptPath = histItemList(self.scriptPath, hist)

        fillIn(self.scriptPath, self.hist)
        fillIn(self.scriptPathList, self.hist)
        #fillIn(self.promptString,self.promptHist)
        #self.scriptPath.SetStringSelection(self.hist[0])
    
    def OnOkButButton(self, event):
        #print '---------------------%s'%self.path
        self.path = self.scriptPath.GetStringSelection()
        self.delay = self.timeoutSetting.GetValue()
        self.pattern = self.promptString.GetStringSelection()
        self.Show(False)
        event.Skip()

    def OnBrowserButButton(self, event):
        #Select a file
        import os
        dlg = wx.FileDialog(
            self, message="Choose a file", defaultDir=os.getcwd(),
            defaultFile="", wildcard="All files (*.*)|*.*",
            style=wx.OPEN | wx.CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            #print 'You selected file is %s:' % (path)
            if path:#open a file
                #self.pathSelected = path
                insertNew(self.scriptPath, path)
                insertNew(self.scriptPathList, path)
                self.hist.append(path)
                
        event.Skip()
    def GetPath(self):
        return self.path
