
from twisted.conch.ui import ansi

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='d:\\log.txt',
                    filemode='w')

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


class rtfTextAdapter():
    def __init__(self, styledTextCtrl):
        self.ctrl = styledTextCtrl
        self.connection  = None #When connecting protocol will set this value to connection
        self.ansiParser = ansi.AnsiParser(ansi.ColorText.WHITE, ansi.ColorText.BLACK)
        self.ansiParser.writeString = self.writeString
        self.ansiParser.parseCursor = self.parseCursor
        self.ansiParser.parseErase = self.parseErase
        #connectTelnet(session, self)
        self.x = 0
        self.y = 0
        

    def write(self, data):
        #logging.error('data:')
        #logging.error(data)
        self.ansiParser.parseString(data)
        
    def _write(self, ch, fg, bg):
        #logging.error('_write called:'+ch)
        logging.error('fg, bg: %s, %s'%(fg, bg))
        #import wx
        #color = wx.Colour()
        #color.Set(fg)
        self.ctrl.BeginTextColour(fg)
        self.ctrl.AppendText(ch)
        #self.ctrl.EndStyle()

        #self.ctrl.DocumentEnd()
    
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
        
    def char(self, event):
        if self.connection and event.KeyCode:
            self.connection.write(chr(event.KeyCode))
            logging.error(chr(event.KeyCode))
            
    def keyDown(self, event):
        if self.connection and event.KeyCode == 13:#Enter
            self.connection.write(chr(event.KeyCode))
            logging.error('entered:%c,%d'%(chr(event.KeyCode),event.KeyCode))
            return
        event.Skip()
