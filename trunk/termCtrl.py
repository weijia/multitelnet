#Boa:Frame:termWin

import wx
from wx.lib.anchors import LayoutAnchors
import wx.stc
import string
from styledTextCtrlAdapterV3 import *

def create(parent):
    return termWin(parent)

[wxID_TERMWIN, wxID_TERMWINTERMWINCMDCOMBO, wxID_TERMWINTERMWINCONTENT, 
 wxID_TERMWINTERMWINHISTLIST, wxID_TERMWINTERMWINSPLITTER, 
 wxID_TERMWINTERMWINTOOLBAR, 
] = [wx.NewId() for _init_ctrls in range(6)]

[wxID_TERMWINTERMWINTOOLBARCOMMANDLIST, wxID_TERMWINTERMWINTOOLBAROPENLOG, 
 wxID_TERMWINTERMWINTOOLBARSELECTFONT, wxID_TERMWINTERMWINTOOLBARTOOLS2, 
] = [wx.NewId() for _init_coll_termWinToolBar_Tools in range(4)]

#Images are get from http://www.iconarchive.com/show/glaze-icons-by-mart/font-bitmap-icon.html

class termWin(wx.Frame):
    def _init_coll_termWinToolBar_Tools(self, parent):
        # generated method, don't edit

        parent.DoAddTool(bitmap=wx.Bitmap(u'Log.png', wx.BITMAP_TYPE_PNG),
              bmpDisabled=wx.NullBitmap,
              id=wxID_TERMWINTERMWINTOOLBARCOMMANDLIST, kind=wx.ITEM_NORMAL,
              label='', longHelp=u'', shortHelp=u'Open Command list')
        parent.DoAddTool(bitmap=wx.Bitmap(u'font-bitmap-16x16.png',
              wx.BITMAP_TYPE_PNG), bmpDisabled=wx.NullBitmap,
              id=wxID_TERMWINTERMWINTOOLBARSELECTFONT, kind=wx.ITEM_NORMAL,
              label='', longHelp='', shortHelp=u'Select Font')
        parent.DoAddTool(bitmap=wx.Bitmap(u'gf-16x16.png', wx.BITMAP_TYPE_PNG),
              bmpDisabled=wx.NullBitmap, id=wxID_TERMWINTERMWINTOOLBARTOOLS2,
              kind=wx.ITEM_CHECK, label=u'debug', longHelp='',
              shortHelp=u'enableDebug')
        parent.DoAddTool(bitmap=wx.Bitmap(u'log-16x16.png',
              wx.BITMAP_TYPE_PNG), bmpDisabled=wx.NullBitmap,
              id=wxID_TERMWINTERMWINTOOLBAROPENLOG, kind=wx.ITEM_NORMAL,
              label=u'openLogFile', longHelp='', shortHelp=u'open log file')
        self.Bind(wx.EVT_TOOL, self.OnToolBar1Tools0Tool,
              id=wxID_TERMWINTERMWINTOOLBARCOMMANDLIST)
        self.Bind(wx.EVT_TOOL, self.OnTermWinToolBarSelectfontTool,
              id=wxID_TERMWINTERMWINTOOLBARSELECTFONT)
        self.Bind(wx.EVT_TOOL, self.OnTermWinToolBarTools2Tool,
              id=wxID_TERMWINTERMWINTOOLBARTOOLS2)
        self.Bind(wx.EVT_TOOL, self.OnTermWinToolBarOpenlogTool,
              id=wxID_TERMWINTERMWINTOOLBAROPENLOG)

        parent.Realize()

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_TERMWIN, name=u'termWin', parent=prnt,
              pos=wx.Point(436, 248), size=wx.Size(753, 563),
              style=wx.DEFAULT_FRAME_STYLE, title=u'termWin')
        self.SetClientSize(wx.Size(745, 536))
        self.SetAutoLayout(True)
        self.Bind(wx.EVT_CLOSE, self.OnTermWinClose)

        self.termWinToolBar = wx.ToolBar(id=wxID_TERMWINTERMWINTOOLBAR,
              name=u'termWinToolBar', parent=self, pos=wx.Point(0, 0),
              size=wx.Size(745, 27), style=wx.TB_HORIZONTAL | wx.NO_BORDER)
        self.SetToolBar(self.termWinToolBar)

        self.termWinSplitter = wx.SplitterWindow(id=wxID_TERMWINTERMWINSPLITTER,
              name=u'termWinSplitter', parent=self, pos=wx.Point(0, 0),
              size=wx.Size(744, 488), style=wx.SP_3D)
        self.termWinSplitter.SetConstraints(LayoutAnchors(self.termWinSplitter,
              True, True, True, True))

        self.termWinContent = wx.stc.StyledTextCtrl(id=wxID_TERMWINTERMWINCONTENT,
              name=u'termWinContent', parent=self.termWinSplitter,
              pos=wx.Point(2, 2), size=wx.Size(740, 348), style=0)
        self.termWinContent.SetMinSize(wx.Size(-1, -1))
        self.termWinContent.SetUseHorizontalScrollBar(True)
        self.termWinContent.Bind(wx.EVT_KEY_DOWN, self.OnTermWinContentKeyDown)
        self.termWinContent.Bind(wx.EVT_CHAR, self.OnTermWinContentChar)
        self.termWinContent.Bind(wx.EVT_RIGHT_DOWN,
              self.OnTermWinContentRightDown)
        self.termWinContent.Bind(wx.EVT_LEFT_UP, self.OnTermWinContentLeftUp)
        self.termWinContent.Bind(wx.EVT_LEFT_DOWN,
              self.OnTermWinContentLeftDown)
        self.termWinContent.Bind(wx.EVT_RIGHT_UP, self.OnTermWinContentRightUp)

        self.termWinHistList = wx.ListBox(choices=[],
              id=wxID_TERMWINTERMWINHISTLIST, name=u'termWinHistList',
              parent=self.termWinSplitter, pos=wx.Point(2, 357),
              size=wx.Size(740, 129), style=0)
        self.termWinHistList.SetMinSize(wx.Size(-1, -1))
        self.termWinSplitter.SplitHorizontally(self.termWinContent,
              self.termWinHistList, 350)

        self.termWinCmdCombo = wx.ComboBox(choices=[],
              id=wxID_TERMWINTERMWINCMDCOMBO, name=u'termWinCmdCombo',
              parent=self, pos=wx.Point(0, 489), size=wx.Size(747, 21), style=0,
              value='')
        self.termWinCmdCombo.SetConstraints(LayoutAnchors(self.termWinCmdCombo,
              True, False, True, True))
        self.termWinCmdCombo.Bind(wx.EVT_TEXT, self.OnTermWinCmdComboText,
              id=wxID_TERMWINTERMWINCMDCOMBO)
        self.termWinCmdCombo.Bind(wx.EVT_CHAR, self.OnTermWinCmdComboChar)
        self.termWinCmdCombo.Bind(wx.EVT_TEXT_ENTER,
              self.OnTermWinCmdComboTextEnter, id=wxID_TERMWINTERMWINCMDCOMBO)

        self._init_coll_termWinToolBar_Tools(self.termWinToolBar)

    def __init__(self, parent):
        self._init_ctrls(parent)
        #Init the splitwin
        #self.termWinSplitter.SetSashPosition(self.termWinSplitter.)
        faces = { 'times': 'Times',
                  'mono' : 'Courier New',
                  'helv' : 'Helvetica',
                  'other': 'new century schoolbook',
                  'size' : 14,
                  'size2': 10,
                 }
        '''
        lc = wx.LayoutConstraints()
        lc.left.SameAs(self.termWinSplitter, wx.Left)
        lc.right.SameAs(self.termWinSplitter, wx.Right)
        lc.top.SameAs(self.termWinSplitter, wx.Bottom)

        self.termWinCmdCombo.SetConstraints(lc)
        '''
        self.termWinCmdCombo.SetAutoLayout(True)
        # Global default styles for all languages
        self.fontName = 'Courier New'
        self.termWinContent.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT,"face:%(mono)s,size:%(size)d,size2:14" % faces)
        self.termWinContent.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT,"fore:white,back:black")
        self.termWinContent.StyleSetSpec(0,"fore:white,back:black,size:14,size2:14")#add any non-style text will set style to 0
        #self.termWinContent.StyleSetBackground(wx.stc.STC_STYLE_DEFAULT,'#000000')
        self.termWinContent.SetMarginType(0, wx.stc.STC_MARGIN_NUMBER)
        self.termWinContent.SetMarginWidth(0, 40)
        self.termWinSplitter.Unsplit()#Unsplit by default
        self.termWinContent.SetCaretWidth(8)
        self.termWinContent.SetCaretLineVisible(True)
        #self.termWinContent.SetBackgroundColour(wx.Colour(255, 255, 255))
        #self.termWinContent.SetForegroundColour(wx.Colour(255, 255, 255))
        try:#The following will not run correctly in linux
            self.termWinContent.SetCaretLineBackground(wx.Colour(0, 51, 255))
        except:
            pass
        self.curSize = None
        self.targetSize = None
        self.termWinContent.frame = self
        self.termWinContent.cursorUpdated = True
        #self.termWinContent.SetEOLMode(wx.stc.STC_EOL_CR)
        self.termWinContent.SetSelAlpha(128)
        self.enterFlag = False
        self.adapter = None
        self.session = None
        self.configuration = None
        self.vwManager = None


    def OnToolBar1Tools0Tool(self, event):
        #Fist button of the toolbar
        #self.adapter.runScript()
        self.vwManager.runScript(self)
        event.Skip()

    def OnTermWinClose(self, event):
        print '-------------------------closing frame'
        try:
            self.adapter.saveAll()
            if self.adapter.connected:
                self.adapter.connection.loseConnection()
            if self.vwManager != None:
                self.vwManager.onViewClose()
        except:
            pass
        event.Skip()
    
    def OnTermWinCmdComboText(self, event):
        print 'combo text'
        if self.enterFlag:
            print 'skip first'
            event.Skip()
        if not self.backspaceFlag:
            exist = self.termWinCmdCombo.GetValue()
            try:
                if len(exist) < self.session['leastAutoComplete']:
                    event.Skip()
            except:
                self.session['leastAutoComplete'] = 5#default value
                event.Skip()
            #print 'current value%s'%exist
            items = self.termWinCmdCombo.GetItems()
            for i in items:
                #print i
                if string.find(i, exist) == 0:
                    #print 'find one:%s, %s'%(i,exist)
                    self.termWinCmdCombo.SetValue(i)
                    self.termWinCmdCombo.SetMark(len(exist), len(i))
                    print 'comb text return'
                    return
        print 'skip'
        event.Skip()

    def linuxOnTermWinCmdComboText(self, event):
        print 'combo text'
        #Prevent the search again after autocomplete change the text
        if not self.startAutoCompleteFlag:
            print 'skip auto complete'
            self.startAutoCompleteFlag = True
            event.Skip()
            return
        
        
        if not self.backspaceFlag:
            exist = self.termWinCmdCombo.GetValue()
            print 'exist:%s, len:%d'%(exist,len(exist))
            if len(exist) < 1:#The function will be called twice in linux after a char is inputed
                event.Skip()
                print 'first event ignore'
                return
            try:
                #if len(exist) < self.session['leastAutoComplete']:
                if False:
                    event.Skip()
                    return
            except:
                self.session['leastAutoComplete'] = 5#default value
                print 'no leastAuto setting return'
                event.Skip()
                return
            #print 'current value%s'%exist
            #try:
            if self.termWinCmdCombo.GetCount() > 0:
                items = self.termWinCmdCombo.GetStrings()
                for i in items:
                    print 'exist:%s,hist:%s'%(exist,i)
                    if string.find(i, exist) == 0:
                        print 'find one:%s, %s'%(i,exist)
                        self.startAutoCompleteFlag = False
                        self.termWinCmdCombo.SetValue(i)#This function will call combo text again..
                        print 'set value ok'
                        self.termWinCmdCombo.SetMark(len(exist), len(i))
                        print 'set mark ok'
                        #self.startAutoCompleteFlag = False
                        print 'exist len:%d, total:%d'%(len(exist),len(i))
                        print 'comb text return'
                        return
        print 'skip'
        event.Skip()

    def OnTermWinCmdComboChar(self, event):
        print 'combo char'
        curKey = event.GetKeyCode()
        print 'char:%d'%curKey
        if curKey != wx.WXK_BACK:
            self.backspaceFlag = False
        else:
            self.backspaceFlag = True
        '''
        if curKey == wx.WXK_DELETE:
            print 'delete pressed, index is%d'%self.termWinCmdCombo.GetSelection()
            self.termWinCmdCombo.Delete(self.termWinCmdCombo.GetSelection())
        '''
        if curKey == wx.WXK_RETURN:
            self.enterFlag = True
        event.Skip()



    def OnTermWinContentKeyDown(self, event):
        self.adapter.keyDown(event)
        #event.Skip()

    def OnTermWinContentChar(self, event):
        self.adapter.char(event)
        #event.Skip()



    def pasteClipboard(self):
        print 'pasteClipboard called'
        text_data = wx.TextDataObject()
        if wx.TheClipboard.Open():
            success = wx.TheClipboard.GetData(text_data) 
            wx.TheClipboard.Close() 
        if success:
            self.adapter.sendString(text_data.GetText().encode('utf8'))



    def OnTermWinContentLeftUp(self, event):
        self.termWinContent.cursorUpdated = True
        '''
        #self.termWinContent.Unbind(wx.EVT_MOTION, self.OntermWinContentMotion)
        if self.leftMouseMotion:#Moved so maybe there is text selected
            #Set selected text to clipboard
            #Set the flag to default value
            self.leftMouseMotion = False
        '''
        #Paste if selected
        obj = wx.TextDataObject(self.termWinContent.GetSelectedText())
        wx.TheClipboard.SetData(obj)
        event.Skip()

    def OnTermWinContentLeftDown(self, event):
        self.leftMouseDown = True#Do we need this?
        self.termWinContent.cursorUpdated = True
        event.Skip()

    def OnTermWinCmdComboTextEnter(self, event):
        print 'term ctrl:string enter'
        va = self.termWinCmdCombo.GetValue()
        self.termWinCmdCombo.SelectAll()
        #if wx.NOT_FOUND == self.termWinCmdCombo.FindString(va):#It is the history, so it should contain dup information
        self.termWinCmdCombo.Insert(va, 0)#we will even add single enter character
        #event.Skip()#If we do not skip there will be an beep
        #remove the element first and append it again. If we need to record the actions
        #user made, use a record button in the future.
        try:
            while True:
                self.session['cmdHist'].remove(va)
        except ValueError:
            print 'term ctrl: no value'
            pass
        self.session['cmdHist'].insert(0, va)
        try:
            self.session['cmdHistState'][va] += 1
        except KeyError:
            #The dict of self.session['cmdHistState'] is inited in above for sure
            self.session['cmdHistState'][va] = 1

        #print 'command history:'+va
        self.adapter.stringEntered(va)
        #event.Skip()#This statement will cause combo to generate a bell

    def title(self, s):
        self.SetTitle(s)

    def OnTermWinToolBarSelectfontTool(self, event):
        fontdata = wx.FontData()
        fontdata.GetChosenFont().SetFaceName(self.fontName)
        #fontdata.SetChosenFont()
        font = wx.FontDialog(self,fontdata)
        if font.ShowModal() == wx.ID_OK:
            fontdata = font.GetFontData()
            print fontdata.GetChosenFont().GetFaceName()
            for i in range(16):
                self.termWinContent.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT,
                    "face:%s"%fontdata.GetChosenFont().GetFaceName())
            #self.termWinContent.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT,"fore:white,back:black")
        self.fontName = fontdata.GetChosenFont().GetFaceName()
        event.Skip()

    def OnTermWinContentRightUp(self, event):
        #Disable the right click menu
        #event.Skip()
        #self.adapter.rightMouseDown(event)
        pass
        
    def OnTermWinContentRightDown(self, event):
        self.termWinContent.cursorUpdated = True
        self.adapter.rightMouseDown(event)    
        #event.Skip()
        
    def OnTermWinToolBarTools2Tool(self, event):
        self.adapter.switchDebug()
        #event.Skip()

    def OnTermWinToolBarOpenlogTool(self, event):
        self.adapter.openLogFile()
        event.Skip()
    
    def initCmdHist(self, hist):
        '''
        Add commands in history to list box
        '''
        items = hist.items()
        items.sort()
        #Sort the commands according to the use frequency
        backitems=[ [v[1],v[0]] for v in items]
        backitems.sort()
        '''
        for j in items:
            print "key,value:%d,%s"%(j[1], j[0])
        '''
        for v in backitems:
            #print v[1]
            self.termWinCmdCombo.Insert(v[1],0)

    def initSession(self, config, session, vwManager = None):
        self.adapter = styledTextAdapter(self.termWinContent, config, session)
        self.session = session
        self.configuration = config
        self.initCmdHist(session['cmdHistState'])
        self.title(session['sessionName'])
        self.dataReceived = self.adapter.dataReceived
        self.write = self.dataReceived
        self.setTermType = self.adapter.setTermType
        self.vwManager = vwManager
        

        
    def getPassword(self):
        self.getPassDefer = defer.Deferred()
        #self.getPassFlag = True
        return self.getPassDefer

    def onDisconnected(self, reason):
        '''
        self.connected = False
        try:
            reason.printTraceback()
        except:
            traceback.print_exc(file=self.appLog)
            traceback.print_exc(file=sys.stdout)
        try:
            self.writeString(reason.getTraceBack(), '#ffffff', '#000000')
        except:
            traceback.print_exc(file=self.appLog)
            traceback.print_exc(file=sys.stdout)
        try:
            self.writeString(reason.printTraceback(file=self.appLog), '#ffffff', '#000000')
        except:
            traceback.print_exc(file=self.appLog)
            traceback.print_exc(file=sys.stdout)

        try:
            self.writeString("client connection lost"+str(reason), '#ffffff', '#000000')
            self.log("client connection lost"+str(reason))
        except:
            traceback.print_exc(file=self.appLog)
            traceback.print_exc(file=sys.stdout)
        '''
        self.title(self.session['sessionName']+"client connection lost" + str(reason))
