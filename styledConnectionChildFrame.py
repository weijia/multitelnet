#Boa:MDIChild:styledConnectionChildFrame

import wx
from wx.lib.anchors import LayoutAnchors
import wx.stc
import string



def create(parent):
    return styledConnectionChildFrame(parent)

[wxID_STYLEDCONNECTIONCHILDFRAME, wxID_STYLEDCONNECTIONCHILDFRAMECOMBOBOX1, 
 wxID_STYLEDCONNECTIONCHILDFRAMELISTBOX1, 
 wxID_STYLEDCONNECTIONCHILDFRAMESPLITTERWINDOW1, 
 wxID_STYLEDCONNECTIONCHILDFRAMESTYLEDTEXTCTRL1, 
 wxID_STYLEDCONNECTIONCHILDFRAMETOOLBAR1, 
] = [wx.NewId() for _init_ctrls in range(6)]

[wxID_STYLEDCONNECTIONCHILDFRAMETOOLBAR1HISTORYLIST, 
 wxID_STYLEDCONNECTIONCHILDFRAMETOOLBAR1TOOLS1, 
] = [wx.NewId() for _init_coll_toolBar1_Tools in range(2)]

class styledConnectionChildFrame(wx.MDIChildFrame):
    def _init_coll_toolBar1_Tools(self, parent):
        # generated method, don't edit

        parent.DoAddTool(bitmap=wx.Bitmap(u'Log.png', wx.BITMAP_TYPE_PNG),
              bmpDisabled=wx.Bitmap(u'Log.png', wx.BITMAP_TYPE_PNG),
              id=wxID_STYLEDCONNECTIONCHILDFRAMETOOLBAR1HISTORYLIST,
              kind=wx.ITEM_NORMAL, label=u'', longHelp='',
              shortHelp=u'History list')
        parent.DoAddTool(bitmap=wx.Bitmap(u'Log.png', wx.BITMAP_TYPE_PNG),
              bmpDisabled=wx.NullBitmap,
              id=wxID_STYLEDCONNECTIONCHILDFRAMETOOLBAR1TOOLS1,
              kind=wx.ITEM_NORMAL, label=u'auto script', longHelp='',
              shortHelp=u'Auto script')
        self.Bind(wx.EVT_TOOL, self.OnToolBar1HistorylistTool,
              id=wxID_STYLEDCONNECTIONCHILDFRAMETOOLBAR1HISTORYLIST)
        self.Bind(wx.EVT_TOOL, self.OnToolBar1Tools1Tool,
              id=wxID_STYLEDCONNECTIONCHILDFRAMETOOLBAR1TOOLS1)

        parent.Realize()

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.MDIChildFrame.__init__(self, id=wxID_STYLEDCONNECTIONCHILDFRAME,
              name=u'styledConnectionChildFrame', parent=prnt, pos=wx.Point(483,
              235), size=wx.Size(443, 443),
              style=wx.MAXIMIZE | wx.DEFAULT_FRAME_STYLE,
              title=u'ConnectionFrame')
        self.SetClientSize(wx.Size(435, 416))
        self.SetAutoLayout(True)
        self.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              u'Terminal'))
        #self.Bind(wx.EVT_ACTIVATE, self.OnStyledConnectionChildFrameActivate)
        self.Bind(wx.EVT_CLOSE, self.OnStyledConnectionChildFrameClose)

        self.splitterWindow1 = wx.SplitterWindow(id=wxID_STYLEDCONNECTIONCHILDFRAMESPLITTERWINDOW1,
              name='splitterWindow1', parent=self, pos=wx.Point(0, 0),
              size=wx.Size(434, 384), style=wx.SP_3D)
        self.splitterWindow1.SetAutoLayout(True)
        self.splitterWindow1.SetConstraints(LayoutAnchors(self.splitterWindow1,
              True, True, True, True))
        self.splitterWindow1.SetNeedUpdating(True)
        self.splitterWindow1.Bind(wx.EVT_SPLITTER_DOUBLECLICKED,
              self.OnSplitterWindow1SplitterDoubleclicked,
              id=wxID_STYLEDCONNECTIONCHILDFRAMESPLITTERWINDOW1)
        self.splitterWindow1.Bind(wx.EVT_SIZE, self.OnSplitterWindow1Size)

        self.listBox1 = wx.ListBox(choices=[],
              id=wxID_STYLEDCONNECTIONCHILDFRAMELISTBOX1, name='listBox1',
              parent=self.splitterWindow1, pos=wx.Point(2, 157),
              size=wx.Size(430, 225), style=0)
        self.listBox1.SetMaxSize(wx.Size(-1, 100))
        self.listBox1.SetMinSize(wx.Size(-1, -1))
        self.listBox1.Bind(wx.EVT_LEFT_DCLICK, self.OnListBox1LeftDclick)

        self.styledTextCtrl1 = wx.stc.StyledTextCtrl(id=wxID_STYLEDCONNECTIONCHILDFRAMESTYLEDTEXTCTRL1,
              name='styledTextCtrl1', parent=self.splitterWindow1,
              pos=wx.Point(2, 2), size=wx.Size(430, 148), style=0)
        self.styledTextCtrl1.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.styledTextCtrl1.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, u'Terminal'))
        self.styledTextCtrl1.SetCaretWidth(8)
        self.styledTextCtrl1.SetForegroundColour(wx.Colour(255, 255, 255))
        self.styledTextCtrl1.SetCaretLineVisible(True)
        self.styledTextCtrl1.SetAutoLayout(True)
        self.styledTextCtrl1.SetBackgroundStyle(wx.BG_STYLE_SYSTEM)
        self.styledTextCtrl1.SetCaretLineBackground(wx.Colour(0, 51, 255))
        self.styledTextCtrl1.SetMinSize(wx.Size(-1, -1))
        self.styledTextCtrl1.SetEdgeMode(wx.stc.STC_EDGE_LINE)
        self.styledTextCtrl1.Bind(wx.EVT_KEY_DOWN,
              self.OnStyledTextCtrl1KeyDown)
        self.styledTextCtrl1.Bind(wx.EVT_CHAR, self.OnStyledTextCtrl1Char)
        self.styledTextCtrl1.Bind(wx.EVT_RIGHT_DOWN,
              self.OnStyledTextCtrl1RightDown)
        self.styledTextCtrl1.Bind(wx.EVT_LEFT_UP, self.OnStyledTextCtrl1LeftUp)
        self.styledTextCtrl1.Bind(wx.EVT_RIGHT_UP,
              self.OnStyledTextCtrl1RightUp)
        self.splitterWindow1.SplitHorizontally(self.styledTextCtrl1,
              self.listBox1, 150)

        self.comboBox1 = wx.ComboBox(choices=[],
              id=wxID_STYLEDCONNECTIONCHILDFRAMECOMBOBOX1, name='comboBox1',
              parent=self, pos=wx.Point(2, 389), size=wx.Size(430, 24), style=0,
              value=u'')
        self.comboBox1.SetConstraints(LayoutAnchors(self.comboBox1, True, False,
              True, True))
        self.comboBox1.SetLabel(u'')
        self.comboBox1.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, u'Tahoma'))
        self.comboBox1.Bind(wx.EVT_TEXT_ENTER, self.OnComboBox1TextEnter,
              id=wxID_STYLEDCONNECTIONCHILDFRAMECOMBOBOX1)
        self.comboBox1.Bind(wx.EVT_RIGHT_DOWN, self.OnComboBox1RightDown)
        self.comboBox1.Bind(wx.EVT_CHAR, self.OnComboBox1Char)
        self.comboBox1.Bind(wx.EVT_TEXT, self.OnComboBox1Text,
              id=wxID_STYLEDCONNECTIONCHILDFRAMECOMBOBOX1)

        self.toolBar1 = wx.ToolBar(id=wxID_STYLEDCONNECTIONCHILDFRAMETOOLBAR1,
              name='toolBar1', parent=self, pos=wx.Point(0, 0),
              size=wx.Size(435, 27), style=wx.TB_HORIZONTAL | wx.NO_BORDER)
        self.SetToolBar(self.toolBar1)

        self._init_coll_toolBar1_Tools(self.toolBar1)

    def __init__(self, parent):
        self._init_ctrls(parent)
        '''
        from wxConsoleControl import wxConsoleControl
        self.styledTextCtrl1 = wxConsoleControl(id=wxID_STYLEDCONNECTIONCHILDFRAMESTYLEDTEXTCTRL1,
              name='styledTextCtrl1', parent=self, pos=wx.Point(0, 0),
              size=wx.Size(392, 224), style=0)
        '''
        faces = { 'times': 'Times',
                  'mono' : 'Courier',
                  'helv' : 'Helvetica',
                  'other': 'new century schoolbook',
                  'size' : 12,
                  'size2': 10,
                 }


        # Global default styles for all languages
        self.styledTextCtrl1.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT,"face:%(helv)s,size:%(size)d" % faces)
        self.styledTextCtrl1.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT,"fore:white,back:black")
        self.styledTextCtrl1.StyleSetSpec(0,"fore:white,back:black")#add any non-style text will set style to 0
        #self.styledTextCtrl1.StyleSetBackground(wx.stc.STC_STYLE_DEFAULT,'#000000')
        self.styledTextCtrl1.SetMarginType(0, wx.stc.STC_MARGIN_NUMBER)
        self.styledTextCtrl1.SetMarginWidth(0, 40)
        self.splitterWindow1.Unsplit()#Unsplit by default
        self.curSize = None
        self.targetSize = None


    def connect(self, configuration, session):
        self.session = session
        self.configuration = configuration
        from styledTextCtrlAdapterV2 import styledTextAdapter
        self.adapter = styledTextAdapter(self.styledTextCtrl1, self.configuration, session)
        from telnetConnector import connectTelnet
        for i in self.session['cmdHist']:
            #print 'command history'+i
            self.comboBox1.Insert(i, 0)
            #print i
            #Move to new setting
            try:
                try:
                    if self.session['cmdHistState'][i] != 0:
                        #session history statistics exist
                        pass
                except KeyError:
                    self.session['cmdHistState'][i] = 0
            except KeyError:
                self.session['cmdHistState'] = dict()
                self.session['cmdHistState'][i] = 0
        #Add commands to list box
        items = self.session['cmdHistState'].items()
        items.sort()
        backitems=[ [v[1],v[0]] for v in items]
        backitems.sort()
        '''
        for j in items:
            print "key,value:%d,%s"%(j[1], j[0])
        '''
        for v in backitems:
            #print v[1]
            self.listBox1.Insert(v[1],0)


        connectTelnet(session, self.adapter)
        self.SetTitle(self.session['sessionName'])



    def OnStyledConnectionChildFrameActivate(self, event):
        self.GetParent().onChildFrameActivated(self)
        event.Skip()

    def OnComboBox1TextEnter(self, event):
        va = self.comboBox1.GetValue()
        self.comboBox1.SelectAll()
        #if wx.NOT_FOUND == self.comboBox1.FindString(va):#It is the history, so it should contain dup information
        self.comboBox1.Insert(va, 0)#we will even add single enter character
        #event.Skip()#If we do not skip there will be an beep
        #remove the element first and append it again. If we need to record the actions
        #user made, use a record button in the future.
        try:
            while True:
                self.session['cmdHist'].remove(va)
        except ValueError:
            pass
        self.session['cmdHist'].insert(0, va)
        try:
            self.session['cmdHistState'][va] += 1
        except KeyError:
            #The dict of self.session['cmdHistState'] is inited in above for sure
            self.session['cmdHistState'][va] = 1
        
        #print 'command history:'+va
        self.adapter.stringEntered(va)

    def OnStyledTextCtrl1RightDown(self, event):
        #if self.session['rightMouseDown']():
        #print 'rightMouseDown'
        #print self.styledTextCtrl1.GetStyleAt(0)
        event.Skip()

    def OnStyledTextCtrl1LeftDown(self, event):
        self.leftMouseDown = True#Do we need this?
        #self.styledTextCtrl1.Bind(wx.EVT_MOTION, self.OnStyledTextCtrl1Motion)        
        event.Skip()

    def OnStyledTextCtrl1Motion(self, event):
        #self.leftMouseMotion = True
        event.Skip()

    def OnStyledTextCtrl1LeftUp(self, event):
        self.leftMouseDown = False
        '''
        #self.styledTextCtrl1.Unbind(wx.EVT_MOTION, self.OnStyledTextCtrl1Motion)
        if self.leftMouseMotion:#Moved so maybe there is text selected
            #Set selected text to clipboard
            #Set the flag to default value
            self.leftMouseMotion = False
        '''
        #Paste if selected
        obj = wx.TextDataObject(self.styledTextCtrl1.GetSelectedText())
        wx.TheClipboard.SetData(obj)
        event.Skip()

    def OnStyledConnectionChildFrameClose(self, event):
        print '-------------------------closing frame'
        self.adapter.saveAll()
        event.Skip()

    def OnComboBox1RightDown(self, event):
        text_data = wx.TextDataObject()
        if wx.TheClipboard.Open():
            success = wx.TheClipboard.GetData(text_data) 
            wx.TheClipboard.Close() 
        if success:
            va = self.comboBox1.GetValue()
            self.comboBox1.GetValue(text_data.GetText())
        #event.Skip()
    def pasteClipboard(self):
        text_data = wx.TextDataObject()
        if wx.TheClipboard.Open():
            success = wx.TheClipboard.GetData(text_data) 
            wx.TheClipboard.Close() 
        if success:
            self.adapter.stringEntered(text_data.GetText().encode('utf8'))

    def OnStyledTextCtrl1RightUp(self, event):
        self.adapter.rightMouseDown(event)
        #event.Skip()


    def OnSplitterWindow1Size(self, event):
        if self.splitterWindow1.IsSplit():
            self.splitterWindow1.SetSashPosition(self.splitterWindow1.GetSizeTuple()[1]-100)
        event.Skip()

    def OnSplitterWindow1SplitterDoubleclicked(self, event):
        #self.toggleSplit()
        event.Skip()

    def OnToolBar1HistorylistTool(self, event):
        self.toggleSplit()
        event.Skip()

    def toggleSplit(self):
        if self.splitterWindow1.IsSplit():
            self.splitterWindow1.Unsplit()
            #self.splitterWindow1.SetSashPosition(self.splitterWindow1.GetSizeTuple()[1]-20)
        else:
            self.splitterWindow1.SplitHorizontally(self.styledTextCtrl1, self.listBox1, self.splitterWindow1.GetSizeTuple()[1]-100)

    def OnListBox1LeftDclick(self, event):
        self.adapter.stringEntered(self.listBox1.GetStringSelection())
        try:
            self.session['cmdHistState'][self.listBox1.GetStringSelection()] += 1
        except KeyError:
            #The dict of self.session['cmdHistState'] is inited in above for sure
            self.session['cmdHistState'][self.listBox1.GetStringSelection()] = 1        
        event.Skip()

    def OnComboBox1Char(self, event):
        curKey = event.GetKeyCode()
        print 'char:%d'%curKey
        if curKey != wx.WXK_BACK:
            self.backspaceFlag = False
        else:
            self.backspaceFlag = True
        '''
        if curKey == wx.WXK_DELETE:
            print 'delete pressed, index is%d'%self.comboBox1.GetSelection()
            self.comboBox1.Delete(self.comboBox1.GetSelection())
        '''
        event.Skip()

    def OnComboBox1Text(self, event):
        if not self.backspaceFlag:
            exist = self.comboBox1.GetValue()
            try:
                if len(exist) < self.session['leastAutoComplete']:
                    event.Skip()
            except:
                self.session['leastAutoComplete'] = 5#default value
                event.Skip()
            #print 'current value%s'%exist
            items = self.comboBox1.GetItems()
            for i in items:
                #print i
                if string.find(i, exist) == 0:
                    #print 'find one:%s, %s'%(i,exist)
                    self.comboBox1.SetValue(i)
                    self.comboBox1.SetMark(len(exist), len(i))
                    return
        event.Skip()
        
    def runScript(self):
        #Select a file
        from scriptSelectDialog import chooseScript
        dlg = chooseScript(self)
        dlg.initHist(self.session)
        dlg.ShowModal()
        path = dlg.GetPath()
        print '---------------------%s'%path

        #print 'You selected file is %s:' % (path)
        if path:#open a file
            self.adapter.openScript(path,dlg.delay, dlg.pattern)
        dlg.Destroy()
        


    def OnToolBar1Tools1Tool(self, event):
        self.runScript()
        event.Skip()


#-------------------------------------------------------------------------------
#The following is the key events

    def OnStyledTextCtrl1KeyDown(self, event):
        #print 'keydown'
        self.adapter.keyDown(event)#When 'enter' entered, even we do not transfer 'enter' we still will get an enter in the control
        #event.Skip()

    def OnStyledTextCtrl1Char(self, event):
        #print 'char'
        self.adapter.char(event)
        #event.Skip()
        
