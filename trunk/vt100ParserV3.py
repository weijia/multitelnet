from vt100ParserBase import *
import ansiAdv as ansi
import string


class vt100Parser(vt100ParserBase):
    def __init__(self):
        vt100ParserBase.__init__(self)
        self.x = 0
        self.y = 0#real index is from 1 for terminal
        self.screenTop = 0#the current line of the screen top
        self.scrollTop = 0
        self.scrollBottom = 1
        self.tabLength = 4
        #self.cursorMove = True
        self.transChars = chr(8)#chr(13) will go to the beginning of the line
        self.transTable = string.maketrans(self.transChars, chr(8)*len(self.transChars))
        self.gbkTransTable = string.maketrans(chr(0xf4), '?')

    def otherFunc(self, ch):
        if ch == 'M':
            #Move cursor up a line, if it is the first in the scroll region
            #scroll up.
            self.log('y:%d,top:%d'%(self.y,self.scrollTop))
            #print 'y:%d,top:%d'%(self.y,self.scrollTop)
            if self.y == self.scrollTop:#Real terminal y is start from 1
                #print 'y:%d,top:%d'%(self.y,self.scrollTop)
                #self.log('y:%d,top:%d'%(self.y,self.scrollTop))
                #Remove the last line in the scroll region and insert a line on
                #the top of the scroll region
                self.insertLines(1)
                self.home()
                self.log('bottom:%d,y:%d'%(self.scrollBottom, self.y))
                self.lineMove(self.scrollBottom - self.y)
                self.removeLine()#This will cause the cursor to move to the above line of the delted line
                self.lineMove(self.y - self.scrollBottom + 1)
                self.charMove(self.x)
                #raise 'third'
            else:
                self.lineMove(-1)
                self.y -= 1


                    
    def writeText(self, text, fg, bg):
        for ch in text:
            b = ord(ch)
            self.log('c:%d,%c'%(b,ch))
            if b == 7: # bell
                #self.bell()
                print '\a'
                self.log('should beep')
                pass
            elif b == 8 or b == 127: # BS
                self.log('bs received, char left')
                self.charMove(-1)
                self.x -= 1
                if self.x < 0:
                    self.log('self.x below 0')
                    self.x = 0
            elif b == 9: # TAB
                for i in range(self.tabLength):
                    self.writeChar(' ', fg, bg)
                    self.x += 1
            elif b == 10:# New line
                self.log('vt100:new line')
                self.newLineCharReceived()
            elif b == 13:#\r
                self.crCharReceived()
            elif 32 <= b < 127:
                #self._writeAtTheEnd(ch, fg, bg)
                self.writeChar(ch, fg, bg)
                self.x += 1
            elif b > 127:
                self.writeChar('?', fg, bg)
                self.x += 1
            '''
            elif b == 127:
                self.log('127, no op')
            '''
            #self.log('current x:%d'%self.x)
    def newLineCharReceived(self):
        #self.home()
        #self.x = 0#Only chr(13) will move cursor to 0
        self.lineDownWithScroll(1)
        '''
        self.y += 1
        if self.y > self.getHeight():
            self.y = self.getHeight()
        '''
    def outputText(self, outputFunc, text):
        try:
            return outputFunc(text)
        except:
            self.log('trying gb2312')
            try:
                return outputFunc(text.decode('gb2312'))
            except:
                self.log('no decoder')
                try:
                    return outputFunc(text)
                except:
                    return outputFunc('?'*len(text))
    
    def textDecode(self, text):
        try:
            return text.decode('iso-8859-1','repleace').encode('gbk','repleace')
        except:
            return '?'*len(text)


    def startOfLine(self):
        self.home()
        self.x = 0
    def lineDownWithScroll(self, start):
        self.log('cur x:%d'%self.x)
        self.log('scroll top:%d, scroll bottom:%d, height:%d'%(self.scrollTop, self.scrollBottom, self.getHeight()))
        if (self.getHeight() == self.scrollBottom+1) and (0 == self.scrollTop):
            #The scroll area is equal to the current window area
            self.log('linedownwithscroll x:%d'%self.x)
            #self.home()
            self.lineMove(start)
            self.home()
            self.charMove(self.x)
            self.y += start
            if self.y > self.getHeight()-1:
                self.y = self.getHeight()-1
        else:
            #Maybe there is scroll needed
            self.log('y:%d,num:%d,bottom:%d'%(self.y,start,self.scrollBottom))
            if self.y+start > self.scrollBottom:
                #Exceed the scroll area, need scroll
                self.lineMove(self.scrollBottom - self.y+1)#Insert is taken to the next line
                self.log('move:%d'%(self.scrollBottom - self.y))
                #Now the cursor is at the scroll Bottom
                self.insertLines(self.y+start - self.scrollBottom)#After insert cursor is still at the original line
                self.log('insert:%d'%(self.y+start - self.scrollBottom))
                #After insert, the current real y is self.scrollBottom + self.y+start - self.scrollBottom 
                #So cursor is at self.y+start, move up to scrollTop
                self.lineMove(self.scrollTop - self.scrollBottom-1)
                self.log('move again:%d'%(self.scrollTop - self.scrollBottom-1))
                #Remove the lines
                self.removeLines(self.y+start - self.scrollBottom)
                self.log('remove:%d'%(self.y+start - self.scrollBottom))
                #Currently real cursor is at self.scrollTop
                self.lineMove(self.y - self.scrollTop+1)
                self.log('last move:%d'%(self.scrollBottom - self.scrollTop+1))
                self.log('y:%d'%self.y)
            else:
                #No scroll needed
                self.log('linedownwithscroll x:%d'%self.x)
                #self.home()
                self.lineMove(start)
                self.home()
                self.charMove(self.x)
                self.y += start

