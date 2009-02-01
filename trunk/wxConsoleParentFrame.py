#Boa:MDIParent:wxConsoleParentFrame

import wx
from wx.lib.anchors import LayoutAnchors

logPath = 'd:/'

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='d:\\log.txt',
                    filemode='w')

def create(parent, configuration, manager):
    return wxConsoleParentFrame(parent, configuration, manager)

[wxID_WXCONSOLEPARENTFRAME] = [wx.NewId() for _init_ctrls in range(1)]

[wxID_WXCONSOLEPARENTFRAMECONNECTIONSITEMS0] = [wx.NewId() for _init_coll_Connections_Items in range(1)]

[wxID_WXCONSOLEPARENTFRAMEMENU1ITEMS0] = [wx.NewId() for _init_coll_Script_Items in range(1)]

class wxConsoleParentFrame(wx.MDIParentFrame):
    def _init_coll_Script_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=wxID_WXCONSOLEPARENTFRAMEMENU1ITEMS0,
              kind=wx.ITEM_NORMAL, text=u'Script')

    def _init_coll_fileMenu_Menus(self, parent):
        # generated method, don't edit

        parent.Append(menu=self.Connections, title=u'Connections')
        parent.Append(menu=self.Script, title=u'Scripts')

    def _init_coll_Connections_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=wxID_WXCONSOLEPARENTFRAMECONNECTIONSITEMS0,
              kind=wx.ITEM_NORMAL, text=u'New')
        self.Bind(wx.EVT_MENU, self.OnConnectionsItems0Menu,
              id=wxID_WXCONSOLEPARENTFRAMECONNECTIONSITEMS0)

    def _init_sizers(self):
        # generated method, don't edit
        self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)

    def _init_utils(self):
        # generated method, don't edit
        self.fileMenu = wx.MenuBar()

        self.Connections = wx.Menu(title=u'')

        self.Script = wx.Menu(title='')

        self._init_coll_fileMenu_Menus(self.fileMenu)
        self._init_coll_Connections_Items(self.Connections)
        self._init_coll_Script_Items(self.Script)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.MDIParentFrame.__init__(self, id=wxID_WXCONSOLEPARENTFRAME,
              name=u'wxConsoleParentFrame', parent=prnt, pos=wx.Point(489, 286),
              size=wx.Size(666, 533),
              style=wx.MAXIMIZE | wx.CAPTION | wx.DEFAULT_FRAME_STYLE,
              title=u'wxConsoleFrame')
        self._init_utils()
        self.SetClientSize(wx.Size(658, 506))
        self.SetMenuBar(self.fileMenu)
        self.SetAutoLayout(False)
        self.Enable(True)
        self.Bind(wx.EVT_CLOSE, self.OnWxConsoleParentFrameClose)
        self.Bind(wx.EVT_LEFT_UP, self.OnWxConsoleParentFrameLeftUp)

        self._init_sizers()

    def __init__(self, parent, configuration, manager):
        self.childs = list()
        self._init_ctrls(parent)
        self.configuration = configuration
        self.consoleManager = manager
        
    def openSession(self, session):
        from styledConnectionChildFrame import styledConnectionChildFrame
        child = styledConnectionChildFrame(self)
        self.childs.append(child)
        child.connect(self.configuration, session)
        return child#return the opened session


    def OnConnectionsItems0Menu(self, event):
        #session = {'server':'bbs.nju.edu.cn','cmdHist':[],'rightMouseDown':self.rightMouseDown}
        session = {'sessionName':'1xModemCMP','server':'10.192.202.214','port':2004,'cmdHist':[],'rightMouseDown':self.rightMouseDown,
            'ansiLog':logPath+'ansi.log','charLog':logPath+'char.log'}

        #from rtfConnectionChildFrame import rtfConnectionChildFrame
        #Add tab first so when the child frame is created (it will be activated at once), the 
        #child frame can find the new tab, it may also fix the pagechanged issue
        '''
        if len(self.childs) == 0:
            self.notebook1.SetPageText(0, session['server']+':'+str(session['port']))
            self.notebook1.SetSelection(0)
        else:
            self.notebook1.AddPage(imageId=-1, page=wx.StaticText(id=wxID_WXCONSOLEPARENTFRAMESTATICTEXT1,
                  label=u'', name='staticText1', parent=self.notebook1,
                  pos=wx.Point(0, 0), size=wx.Size(0, 13), style=0), select=True,
                  text=session['server']+':'+str(session['port']))
        '''
        #self.openSession(session)
        event.Skip()

    def OnNotebook1NotebookPageChanged(self, event):
        if len(self.childs) != 0:
            print 'notebook change called'
            '''
            logging.error('data:%d'%self.notebook1.GetSelection())
            print event
            print self.notebook1.GetSelection()
            print self.notebook1.GetCurrentPage()
            '''
            if len(self.childs) > event.GetSelection():
                child = self.childs[event.GetSelection()]
                child.SetFocus()
            else:
                print 'error why'
                print 'cur sel:%d'%event.GetSelection()
                print 'cur childs len:%d'%len(self.childs)
        event.Skip()


    def onChildFrameActivated(self, child):
        cnt = 0
        '''
        for i in self.childs:
            if i == child:
                if self.notebook1.GetPageCount() > cnt:
                    try:
                        self.notebook1.SetSelection(cnt)
                    except:
                        print 'selecting %d faild'%cnt
                    break
            cnt += 1
        '''
        
    def rightMouseDown(self):
        return False

    def OnWxConsoleParentFrameClose(self, event):
        for i in self.childs:
            i.OnStyledConnectionChildFrameClose(event)
        self.Show(False)
        if True:
        #if event.CanVeto():
            event.Veto()
        #event.Skip()

    def OnWxConsoleParentFrameLeftUp(self, event):
        print 'parent event left up'
        event.Skip()
