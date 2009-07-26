#Boa:Frame:toolWindow

import wx
import re

logPath = 'd:/'

localSession = {'sessionName':'localhost:2111','server':'localhost','port':2111,'cmdHist':[],
                'rightMouseDown':"copyToClip",
                'ansiLogName':'%(server)s_%(port)s_%(time)s_ansi.log',
                'ansiLog':logPath+'%(server)s_%(port)s_%(time)s_ansi.log',
                'charLog':logPath+'char.log',
                'baseDir':'d:/tmp/','cmdHistState':{},'sshFlag':False}

def create(parent):
    return toolWindow(parent)

[wxID_TOOLWINDOW, wxID_TOOLWINDOWCHECKBOX1, wxID_TOOLWINDOWCOMBOBOX1, 
 wxID_TOOLWINDOWCOMBOBOX2, wxID_TOOLWINDOWCOMBOBOX3, wxID_TOOLWINDOWCOMBOBOX4, 
 wxID_TOOLWINDOWCOMBOBOX5, wxID_TOOLWINDOWCONNECTBUT, 
 wxID_TOOLWINDOWDELBUTTON, wxID_TOOLWINDOWNOTEBOOK1, wxID_TOOLWINDOWPANEL1, 
 wxID_TOOLWINDOWPLAYBACK, wxID_TOOLWINDOWSSHCON, wxID_TOOLWINDOWSTATICTEXT1, 
 wxID_TOOLWINDOWSTATICTEXT2, wxID_TOOLWINDOWSTATICTEXT3, 
 wxID_TOOLWINDOWSTATICTEXT4, wxID_TOOLWINDOWSTATICTEXT5, 
 wxID_TOOLWINDOWTEXTCTRL1, 
] = [wx.NewId() for _init_ctrls in range(19)]

class toolWindow(wx.Frame):
    def _init_coll_notebook1_Pages(self, parent):
        # generated method, don't edit

        parent.AddPage(imageId=-1, page=self.panel1, select=True,
              text=u'Sessions')

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_TOOLWINDOW, name=u'toolWindow',
              parent=prnt, pos=wx.Point(460, 332), size=wx.Size(542, 273),
              style=wx.DEFAULT_FRAME_STYLE, title=u'Connection manager')
        self.SetClientSize(wx.Size(534, 246))
        self.Bind(wx.EVT_CLOSE, self.OnToolWindowClose)

        self.notebook1 = wx.Notebook(id=wxID_TOOLWINDOWNOTEBOOK1,
              name='notebook1', parent=self, pos=wx.Point(0, 0),
              size=wx.Size(534, 246), style=0)
        self.notebook1.SetAutoLayout(True)

        self.panel1 = wx.Panel(id=wxID_TOOLWINDOWPANEL1, name='panel1',
              parent=self.notebook1, pos=wx.Point(0, 0), size=wx.Size(526, 220),
              style=wx.TAB_TRAVERSAL)
        self.panel1.SetAutoLayout(True)

        self.comboBox1 = wx.ComboBox(choices=[], id=wxID_TOOLWINDOWCOMBOBOX1,
              name='comboBox1', parent=self.panel1, pos=wx.Point(16, 8),
              size=wx.Size(296, 21), style=0, value=u'')
        self.comboBox1.SetLabel(u'')
        self.comboBox1.Bind(wx.EVT_COMBOBOX, self.OnComboBox1Combobox,
              id=wxID_TOOLWINDOWCOMBOBOX1)

        self.staticText1 = wx.StaticText(id=wxID_TOOLWINDOWSTATICTEXT1,
              label=u'Server', name='staticText1', parent=self.panel1,
              pos=wx.Point(40, 32), size=wx.Size(33, 13), style=0)

        self.comboBox2 = wx.ComboBox(choices=[], id=wxID_TOOLWINDOWCOMBOBOX2,
              name='comboBox2', parent=self.panel1, pos=wx.Point(88, 32),
              size=wx.Size(224, 21), style=0, value=u'localhost')
        self.comboBox2.SetLabel(u'localhost')
        self.comboBox2.Bind(wx.EVT_TEXT, self.OnComboBox2Text,
              id=wxID_TOOLWINDOWCOMBOBOX2)

        self.staticText2 = wx.StaticText(id=wxID_TOOLWINDOWSTATICTEXT2,
              label=u'port', name='staticText2', parent=self.panel1,
              pos=wx.Point(48, 56), size=wx.Size(21, 13), style=0)

        self.comboBox3 = wx.ComboBox(choices=[], id=wxID_TOOLWINDOWCOMBOBOX3,
              name='comboBox3', parent=self.panel1, pos=wx.Point(88, 56),
              size=wx.Size(216, 21), style=0, value=u'23')
        self.comboBox3.SetLabel(u'23')
        self.comboBox3.Bind(wx.EVT_TEXT, self.OnComboBox3Text,
              id=wxID_TOOLWINDOWCOMBOBOX3)

        self.comboBox4 = wx.ComboBox(choices=[], id=wxID_TOOLWINDOWCOMBOBOX4,
              name='comboBox4', parent=self.panel1, pos=wx.Point(88, 112),
              size=wx.Size(260, 21), style=0,
              value=u'%(server)s_%(port)s_%(time)s_ansi.log')
        self.comboBox4.SetLabel(u'%(server)s_%(port)s_%(time)s_ansi.log')

        self.staticText3 = wx.StaticText(id=wxID_TOOLWINDOWSTATICTEXT3,
              label=u'ansiLogFile', name='staticText3', parent=self.panel1,
              pos=wx.Point(24, 112), size=wx.Size(53, 13), style=0)

        self.staticText4 = wx.StaticText(id=wxID_TOOLWINDOWSTATICTEXT4,
              label=u'LogPath', name='staticText4', parent=self.panel1,
              pos=wx.Point(32, 80), size=wx.Size(40, 13), style=0)

        self.comboBox5 = wx.ComboBox(choices=[], id=wxID_TOOLWINDOWCOMBOBOX5,
              name='comboBox5', parent=self.panel1, pos=wx.Point(88, 80),
              size=wx.Size(200, 21), style=0, value=u'd:/')
        self.comboBox5.SetLabel(u'd:/')

        self.connectBut = wx.Button(id=wxID_TOOLWINDOWCONNECTBUT,
              label=u'Connect', name=u'connectBut', parent=self.panel1,
              pos=wx.Point(64, 176), size=wx.Size(75, 23), style=0)
        self.connectBut.Bind(wx.EVT_BUTTON, self.OnConnectButButton,
              id=wxID_TOOLWINDOWCONNECTBUT)

        self.checkBox1 = wx.CheckBox(id=wxID_TOOLWINDOWCHECKBOX1,
              label=u'AutoUpdateSessionName', name='checkBox1',
              parent=self.panel1, pos=wx.Point(328, 8), size=wx.Size(160, 13),
              style=0)
        self.checkBox1.SetValue(True)
        self.checkBox1.SetToolTipString(u'checkBox1')

        self.staticText5 = wx.StaticText(id=wxID_TOOLWINDOWSTATICTEXT5,
              label=u'logFileResultName', name='staticText5',
              parent=self.panel1, pos=wx.Point(16, 144), size=wx.Size(88, 13),
              style=0)

        self.textCtrl1 = wx.TextCtrl(id=wxID_TOOLWINDOWTEXTCTRL1,
              name='textCtrl1', parent=self.panel1, pos=wx.Point(144, 144),
              size=wx.Size(296, 21), style=0, value=u'')
        self.textCtrl1.SetEditable(False)

        self.delButton = wx.Button(id=wxID_TOOLWINDOWDELBUTTON,
              label=u'Delete session', name=u'delButton', parent=self.panel1,
              pos=wx.Point(440, 40), size=wx.Size(75, 23), style=0)
        self.delButton.Bind(wx.EVT_BUTTON, self.OnDelButtonButton,
              id=wxID_TOOLWINDOWDELBUTTON)

        self.playback = wx.Button(id=wxID_TOOLWINDOWPLAYBACK, label=u'playback',
              name=u'playback', parent=self.panel1, pos=wx.Point(168, 176),
              size=wx.Size(75, 23), style=0)
        self.playback.Bind(wx.EVT_BUTTON, self.OnPlaybackButton,
              id=wxID_TOOLWINDOWPLAYBACK)

        self.sshCon = wx.CheckBox(id=wxID_TOOLWINDOWSSHCON,
              label=u'SSH enabled?', name=u'sshCon', parent=self.panel1,
              pos=wx.Point(312, 64), size=wx.Size(88, 13), style=0)
        self.sshCon.SetValue(False)
        self.sshCon.Bind(wx.EVT_CHECKBOX, self.OnSshConCheckbox,
              id=wxID_TOOLWINDOWSSHCON)

        self._init_coll_notebook1_Pages(self.notebook1)

    def __init__(self, parent):
        self._init_ctrls(parent)
        #self.consoleWin = None
        import os
        self.consoleManager = None
        self.currentPath = os.getcwd()
        self.logPath = os.path.join(self.currentPath,'logs')
        self.configPath = os.path.join(os.getcwd(), 'multiConsole.conf')
        if not os.path.exists(self.logPath):
            os.mkdir(self.logPath)
        localSession['baseDir'] = self.logPath
        #print os.getcwd()
        #Load configuration file
        #print 'loading configs'
        import cPickle
        try:
            self.configuration = cPickle.load(open(self.configPath, 'rb'))
        except IOError:
            self.configuration = {}
            self.configuration['sessions'] = {'localhost:2111':localSession}
            #print 'new config'
            #import Unicode#No use
        i = None
        #Fill in sessions into combobox
        for i in self.configuration['sessions'].keys():
            #print i
            lastSelection = i
            self.comboBox1.Insert(i, 0)
        #Set global debuging flag
        if os.path.exists(os.path.join(os.getcwd(),'debug.txt')):
            #print 'debuging'
            self.configuration['global'] = {'logDetail':True}
        else:
            self.configuration['global'] = {'logDetail':False}
        #Update the current selection
        if i != None:
            self.comboBox1.SetStringSelection(i)
            #print 'Last selection:%s'%i
            self.updateSelection()
            self.updateAnsiLogPath()
        #print '------------------------------------'
        from twisted.internet import reactor
        #reactor.callLater(1, self.autoOpenLocalConnection)
        self.openLater = {}
        
    def autoOpenLocalConnection(self):
        self.comboBox1.SetStringSelection('localhost:2111')
        #self.comboBox1.SetStringSelection('192.168.3.100:23')
        self.updateSelection()
        self.connectSession()
        
    def openSessionLaterCallback(self):
        for i in self.openLater.keys():
            self.consoleManager.openSession(self.openLater[i])
        self.openLater.clear()
        
    
    def fillInSessionInfo(self, session):
        #Update the information in the configuration
        session['sessionName'] = self.comboBox1.GetValue()
        import os
        session['server'] = self.comboBox2.GetValue()
        session['port'] = int(self.comboBox3.GetValue())
        session['baseDir'] = self.comboBox5.GetValue()
        session['ansiLog'] = os.path.join(session['baseDir'],self.comboBox4.GetValue())
        session['sshFlag'] = self.sshCon.IsChecked()

        #self.comboBox1.Insert(self.comboBox1.GetValue(), 0)
        self.comboBox2.Insert(self.comboBox2.GetValue(), 0)
        self.comboBox3.Insert(self.comboBox3.GetValue(), 0)
        self.comboBox4.Insert(self.comboBox4.GetValue(), 0)
        self.comboBox5.Insert(self.comboBox5.GetValue(), 0)
        #Add strings to configuration
        return session
    '''
    def updateSession(self, session):
        #Update the information in the configuration
        session['sessionName'] = self.comboBox1.GetValue()
        import os
        session['server'] = self.comboBox2.GetValue()
        session['port'] = int(self.comboBox3.GetValue())
        session['baseDir'] = self.comboBox5.GetValue()
        session['ansiLog'] = os.path.join(session['baseDir'],self.comboBox4.GetValue())
        session['sshFlag'] = self.sshCon.IsChecked()

        #self.comboBox1.Insert(self.comboBox1.GetValue(), 0)
        self.comboBox2.Insert(self.comboBox2.GetValue(), 0)
        self.comboBox3.Insert(self.comboBox3.GetValue(), 0)
        self.comboBox4.Insert(self.comboBox4.GetValue(), 0)
        self.comboBox5.Insert(self.comboBox5.GetValue(), 0)
        #Add strings to configuration
        return session
    '''
    
    def rightMouseDown(self):
        pass
    def connectSession(self):
        try:
            session = self.configuration['sessions'][self.comboBox1.GetValue()]
        except KeyError:
            session = localSession
        #if self.consoleWin != None:
        #    self.consoleWin.openSession(session)
        #self.consoleWin.Show()
        #Update values
        self.fillInSessionInfo(session)
        self.consoleManager.openSession(session)
        #for i in session['cmdHist']:
        #    print i

    def createTempSession(self, server, port, triggers, timeoutHandler):
        import copy
        session = copy.copy(localSession)
        import uuid
        session['sessionName'] = server+':'+str(port)+'-'+str(uuid.uuid4())+'-temp-session'
        import os
        session['server'] = server
        session['port'] = port
        session['triggers'] = triggers
        session['ansiLog'] = os.path.join(session['baseDir'], session['ansiLogName'])
        if timeoutHandler != None:
            print 'handler provided'
            session['timeoutHandler'] = timeoutHandler
        self.openLater[session['sessionName']] = session
        from twisted.internet import reactor
        reactor.callLater(1, self.openSessionLaterCallback)

    def OnComboBox1Combobox(self, event):
        self.updateSelection()
        event.Skip()
    
    def updateSelection(self):
        sesName = self.comboBox1.GetValue()
        '''
        for i in self.configuration['sessions'].keys():
            print i
        '''
        session = self.configuration['sessions'][sesName]
        self.comboBox2.SetValue(session['server']) 
        self.comboBox3.SetValue(str(session['port']) )
        self.comboBox5.SetValue(session['baseDir']) 
        import os
        self.comboBox4.SetValue(os.path.basename(session['ansiLog']))
        try:
            self.sshCon.SetValue(session['sshFlag'])
        except:
            pass
        '''
        for i in session['cmdHist']:
            print i
        '''
    def OnToolWindowClose(self, event):
        self.consoleManager.closeAll()
        output = open(self.configPath, 'wb')
        #remove all obsoleted session
        for i in self.configuration['sessions'].keys():
            if re.compile('-temp-session$').search(i):
                del self.configuration['sessions'][i]
        # Pickle dictionary using protocol 0.
        import cPickle
        cPickle.dump(self.configuration, output)
        output.close()
        '''
        for i in self.configuration.keys():
            print self.configuration[i]
        '''
        event.Skip()

    def OnComboBox2Char(self, event):
        event.Skip()
        
    def updateAnsiLogPath(self):
        #Auto change log file name
        server = self.comboBox2.GetValue()
        port = self.comboBox3.GetValue()
        import logFilenameGenerator
        self.textCtrl1.SetValue(logFilenameGenerator.logNameGen(
            self.comboBox4.GetValue(), server, port))
        if  self.checkBox1.GetValue():
            server = self.comboBox2.GetValue()
            port = self.comboBox3.GetValue()
            self.comboBox1.SetValue(server+':'+port)

    def OnComboBox2Text(self, event):
        self.updateAnsiLogPath()
        event.Skip()

    def OnComboBox3Text(self, event):
        if self.comboBox3.GetValue() == '22':
            self.sshCon.SetValue(True)
            #self.session['sshFlag'] = True
        else:
            self.sshCon.SetValue(False)
            #self.session['sshFlag'] = False
        self.updateAnsiLogPath()
        #event.Skip()

    def OnDelButtonButton(self, event):
        rmStr = self.comboBox1.GetValue()
        index = self.comboBox1.FindString(rmStr)
        self.comboBox1.Delete(index)
        del self.configuration['sessions'][rmStr]
        for i in self.configuration['sessions'].keys():
            self.comboBox1.SetValue(i)
            self.updateSelection()
            break
        event.Skip()

    def OnPlaybackButton(self, event):
        try:
            session = self.configuration['sessions'][self.comboBox1.GetValue()]
        except KeyError:
            session = localSession
        self.fillInSessionInfo(session)
        self.consoleManager.openPlayBackSession(session)
        event.Skip()

    def OnConnectButButton(self, event):
        #Connect button
        self.connectSession()
        event.Skip()

    def OnSshConCheckbox(self, event):
        event.Skip()


