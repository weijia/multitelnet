#Boa:Frame:frameUsedForAutoCodeGen

import wx
import wx.stc

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='d:\\log.txt',
                    filemode='w')

from twisted.conch.ui import ansi
from telnetConnector import connectTelnet

colorKeys = (
    'b', 'r', 'g', 'y', 'l', 'm', 'c', 'w',
    'B', 'R', 'G', 'Y', 'L', 'M', 'C', 'W'
)

colorMap = {
    'b': '#000000', 'r': '#c40000', 'g': '#00c400', 'y': '#c4c400',
    'l': '#000080', 'm': '#c400c4', 'c': '#00c4c4', 'w': '#c4c4c4',
    'B': '#626262', 'R': '#ff0000', 'G': '#00ff00', 'Y': '#ffff00',
    'L': '#0000ff', 'M': '#ff00ff', 'C': '#00ffff', 'W': '#ffffff',
}

session = {'server':'ftw.mot.com'}



def create(parent):
    return frameUsedForAutoCodeGen(parent)

[wxID_FRAMEUSEDFORAUTOCODEGEN, wxID_FRAMEUSEDFORAUTOCODEGENSTYLEDTEXTCTRL1, 
] = [wx.NewId() for _init_ctrls in range(2)]

class frameUsedForAutoCodeGen(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAMEUSEDFORAUTOCODEGEN,
              name=u'frameUsedForAutoCodeGen', parent=prnt, pos=wx.Point(417,
              253), size=wx.Size(400, 250), style=wx.DEFAULT_FRAME_STYLE,
              title=u'Frame1')
        self.SetClientSize(wx.Size(392, 223))

        self.styledTextCtrl1 = wx.stc.StyledTextCtrl(id=wxID_FRAMEUSEDFORAUTOCODEGENSTYLEDTEXTCTRL1,
              name='styledTextCtrl1', parent=self, pos=wx.Point(0, 0),
              size=wx.Size(392, 223), style=0)
        self.styledTextCtrl1.SetReadOnly(False)
        self.styledTextCtrl1.Bind(wx.EVT_CHAR, self.OnStyledTextCtrl1Char)
        self.styledTextCtrl1.Bind(wx.EVT_KEY_DOWN,
              self.OnStyledTextCtrl1KeyDown)

    def __init__(self, parent, session):
        self._init_ctrls(parent)
        self.ansiParser = ansi.AnsiParser(ansi.ColorText.WHITE, ansi.ColorText.BLACK)
        self.ansiParser.writeString = self.writeString
        self.ansiParser.parseCursor = self.parseCursor
        self.ansiParser.parseErase = self.parseErase
        self.connection  = None
        connectTelnet(session, self)
        self.x = 0
        self.y = 0
        
    def OnStyledTextCtrl1Char(self, event):
        if self.connection and event.KeyCode:
            self.connection.write(chr(event.KeyCode))
            logging.error(chr(event.KeyCode))
        #event.StopPropagation()
        #event.Skip()

    def write(self, data):
        logging.error('data:')
        logging.error(data)
        self.ansiParser.parseString(data)
        
    def _write(self, ch, fg, bg):
        #logging.error('_write called:'+ch)
        self.styledTextCtrl1.AppendText(ch)
        self.styledTextCtrl1.DocumentEnd()
    
    def writeString(self, i):
        #logging.error('writeString called')
        if not i.display:
            return
        fg = colorMap[i.fg]
        bg = i.bg != 'b' and colorMap[i.bg]
        for ch in i.text:
            b = ord(ch)
            if b == 7: # bell
                self.bell() 
            elif b == 8: # BS
                if self.x:
                    self.x-=1
            elif b == 9: # TAB
                [self._write(' ',fg,bg) for i in range(8)]
            elif b == 10:# New line
                self._write(ch, fg, bg)
                '''
                if self.y == self.height-1:
                    self._delete(0,0,self.width,0)
                    [self.canvas.move(x,0,-fontHeight) for x in self.canvas.find_all()]
                else:   
                    self.y+=1
                '''
            elif b == 13:
                self.x = 0
            elif 32 <= b < 127:
                self._write(ch, fg, bg)
        
    def parseErase(self, erase):
        logging.error('parseErase called')
        
    def _delete(self, sx, sy, ex, ey):
        logging.error('_delete called')

    def parseCursor(self, cursor):
        logging.error('parseCursor called')

    def OnStyledTextCtrl1KeyDown(self, event):
        if self.connection and event.KeyCode == 13:#Enter
            self.connection.write(chr(event.KeyCode))
            #logging.error('entered:%c,%d'%(chr(event.KeyCode),event.KeyCode))
            return
        event.StopPropagation()
        event.Skip()

