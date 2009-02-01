
import ansiAdv as ansi
import string

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

'''
vt100TermCtrlKeyMapping = {
    'C': chr(3)
}
'''




class vt100Parser():
    def __init__(self):
        self.ansiParser = ansi.AnsiParser(ansi.ColorText.WHITE, ansi.ColorText.BLACK)
        self.ansiParser.writeString = self.writeStringV3
        self.ansiParser.parseCursor = self.parseCursor
        self.ansiParser.parseErase = self.parseErase
        self.ansiParser.otherFunc = self.otherFunc
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

    def _write(self, ch, fg, bg):
        pass
                    
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
                #self.home()
                #self.x = 0#Only chr(13) will move cursor to 0
                self.lineDownWithScroll(1)
                '''
                self.y += 1
                if self.y > self.getHeight():
                    self.y = self.getHeight()
                '''
            elif b == 13:#\r
                self.home()
                self.x = 0
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

    def writeStringV3(self, i):
        #self.log('i.text:%s'%i.text)
        #self.log('i.text:%s'%i)
        if len(i.text) == 0:
            self.log('no text')
            return
        if not i.display:
            self.log('no display')
            return
        #print 'text:%s'%i.text
        fg = colorMap[i.fg]
        bg = i.bg != 'b' and colorMap[i.bg]
        self.log('i.text:%s'%i.text)
        #Remove bell char and find other char except \r and \n
        #newstr = i.text.translate(self.transTable, chr(7))
        newstr = i.text.replace(chr(7),'').replace(chr(9),' '*self.tabLength)
        self.log('newstr:%s'%newstr)
                
        if newstr.find(chr(8)) != -1:
            #chr(8)exist
            self.log('spacial char exist')
            self.writeText(i.text, fg, bg)
        else:
            #Check if there is single \r or \n
            #1. replace \r\n with chr(8)
            checkstr = newstr.replace('\r\n', chr(8))
            #2. find if there is still \r or \n
            if (checkstr.find('\r') != -1) or (checkstr.find('\n') != -1):
                self.writeText(newstr, fg, bg)
            elif self.scrollBottom+1 != self.getHeight():
                #Need scroll
                self.log('need scroll,bottom:%d, height:%d'%(self.scrollBottom, self.getHeight()))
                self.writeText(i.text, fg, bg)
            else:
                #No special char, output string
                self.log('vt100:y:%d'%self.y)
                self.log('vt100:y:%d'%self.y)
                lnCnt = newstr.count(chr(10))
                self.log('vt100:lines:%d'%lnCnt)
                lastR = checkstr.rfind(chr(8))
                self.log('write string in one call')
                if lastR == -1:
                    #Return not exist
                    self.log('vt100:newstr len:%d'%len(newstr))
                    self.writeString(newstr, fg, bg)
                    self.x += len(newstr)
                else:
                    #String with \r\n
                    self.writeString(newstr, fg, bg)
                    self.x = len(checkstr) - lastR#The length of the last line
                    self.y += checkstr.count(chr(8))
                    if self.y >= self.getHeight():
                        self.y = self.getHeight() - 1
                self.log('cur Y:%d'%self.y)
        #self.log('current x:%d'%self.x)

    def parseErase(self, erase):
        self.cursorMove = True
        self.log('parseErase called'+erase)
        if ';' in erase:
            end = erase[-1]
            parts = erase[:-1].split(';')
            [self.parseErase(x+end) for x in parts]
            return
        start = 0

        if len(erase) > 1:
            start = int(erase[:-1])
        if erase[-1] == 'J':#erase screen
            if start == 0:#erase to the end of the screen
                #self._delete(x,y,self.width,self.height)
                self.log('erase to end of screen from %d,%d'%(self.x,self.y))
                self.eraseToEndOfScreen()
                self.x = 0
                self.y = 0
            else:#erase screen
                #self._delete(0,0,self.width,self.height)
                self.log('erase full screen')
                self.home()
                self.lineMove(-self.y)
                self.eraseToEndOfScreen()
                self.x = 0
                self.y = 0
        elif erase[-1] == 'K':#erase line
            if start == 0:#erase to the end of the line
                #self._delete(x,y,self.width,y)
                self.log('delete to right')
                self.delRight()
            elif start == 1:#erase from the beginning of the line
                #self._delete(0,y,x,y)
                self.log('delte to left')
                self.delLineLeft()
                self.x = 0#erase to the whole line
            else:
                #self._delete(0,y,self.width,y)#value 2, erase the whole line
                self.log('delte the whole line')
                #self.eraseTheWholeLine()
                #The following only clear the current line's content
                self.clearLine()
        elif erase[-1] == 'P':#erase number of letters
            #self._delete(x,y,x+start,y)
            #print 'erase %d chars'%start
            self.delRight()

    def parseCursor(self, cursor):
        self.cursorMove = True
        self.log('parseCursor called'+str(cursor))
        start = 1
#-------------------------------------------------------------------------------
        
        #Check if it is scroll command
        if len(cursor) > 1 and cursor[-1] == 'r':
            #scroll command
            try:
                start,end = map(int, cursor[:-1].split(';'))
                self.log('scroll, start:%d, end:%d'%(start, end))
                self.scrollTop = start - 1
                self.scrollBottom = end - 1
                return
            except:
                return
#-------------------------------------------------------------------------------
        
        if len(cursor) > 1 and cursor[-1]!='H':
            try:
                start = int(cursor[:-1])
            except:
                return
            self.log('start is:%d'%start)
            
        if cursor[-1] == 'C':#Move right
            self.x += start
            self.log('move right')
            self.charRight(start)
            
        elif cursor[-1] == 'D':#Move left
            self.log('move left:%d'%start)
            self.charLeft(start)
            self.x -= start
            
        elif cursor[-1]=='d':#Move up to
            self.log('move up to:%d'%(start-1))
            moveDown = start - 1 -self.y
            self.lineMove(start - 1)
            
        elif cursor[-1]=='G':#Move right to
            self.log('move right to:%d'%(start-1))
            moveRight = start - 1 - self.x
            self.charMove(start - 1)
            
        elif cursor[-1]=='A':
            self.log('move up a line')
            self.y -= start
            self.home()
            #self.log('current x:%d'%self.x)
            if self.y < 0:
                self.log('error move up line, but y < 0')
                self.y = 0
            self.lineMove(-start)
            self.charMove(self.x)
            
        elif cursor[-1]=='H':#Move to
            if len(cursor)>1:#Move to certain
                y,x = map(int, cursor[:-1].split(';'))
                self.log('move to:%d,%d'%(x,y))
                self.log('x now is:%d, move to begin'%self.x)
                #self.charMove(-self.x)
                self.home()
                moveDown = y - 1 - self.y
                self.log('move down:%d'%moveDown)
                self.lineMove(moveDown)
                self.log('move x to:%d'%x)
                self.charMove(x - 1)
                self.x = x - 1
                self.y = y - 1
                #raise 'move cursor, just a step by step'
            else:
                #Move to top left
                self.log('move to left top:%d,%d'%(self.x,self.y))
                self.home()
                self.lineMove(-self.y)
                self.x = 0
                self.y = 0
                
        elif cursor[-1]=='B':#Move down
            self.log('move down:%d'%start)
            self.lineDownWithScroll(start)
        self.log('cur x:%d'%self.x)

    '''
    def lineMoveWithScroll(self, start):
        if self.getHeight() == self.scrollBottom+1:
            #The last line of the screen is the last line of the scroll area
            self.lineMove(start)
            self.y += start
            if self.y >= self.getHeight():
                self.y = self.getHeight() - 1
        else:
            #Need to handle scroll here
            self.log('start:%d'%start)
            if self.y+start > self.scrollBottom:
                #Exceed the scroll area, need scroll
                self.lineMove(self.scrollBottom - self.y)
                #Now the cursor is at the scroll Bottom
                self.log('insert:%d'%(self.y+start - self.scrollBottom))
                self.insertLines(self.y+start - self.scrollBottom)
                #After insert, the current real y is self.scrollBottom + self.y+start - self.scrollBottom 
                #So cursor is at self.y+start, move up to scrollTop
                self.lineMove(self.scrollTop - self.y+start)
                #Remove the lines
                self.removeLine(self.y+start - self.scrollBottom)
                #Currently real cursor is at self.scrollTop
                self.lineMove(self.Bottom - self.scrollTop)
    '''
    def lineDownWithScroll(self, start):
        self.log('cur x:%d'%self.x)
        self.log('scroll top:%d, scroll bottom:%d, height:%d'%(self.scrollTop, self.scrollBottom, self.getHeight()))
        if (self.getHeight() == self.scrollBottom+1) and (0 == self.scrollTop):
            #The scroll area is equal to the window
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

    def log(self, str):
        pass

#-------------------------------------------------------------------------------
    def charMove(self, num):
        pass
    def lineMove(self, num):#num<0, move up, num>0 move down
        pass
    def delLeft(self):
        pass
    def delRight(self):
        pass
    def eraseToEndOfScreen(self):
        pass
    def eraseFullScreen(self):
        pass
    def delRight(self, num):
        pass
    def removeLine(self):
        pass
    def writeChar(self, char):
        pass
    def clearLine(self):
        pass
    def getHeight(self):
        pass
    def insertLines(self, num):
        pass
    def removeLines(self, num):
        pass