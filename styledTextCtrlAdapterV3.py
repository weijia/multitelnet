#-----------------------------------------------------------------------------
# Name:        styledTextCtrlAdapter.py
# Purpose:     
#
# Author:      <Weijia Wang>
#
# Created:     2008/09/13
# RCS-ID:      $Id: styledTextCtrlAdapter.py $
# Copyright:   (c) 2008
# Licence:     TBD
#-----------------------------------------------------------------------------

#from twisted.conch.ui import ansi
import ansiAdv as ansi
from vt100ParserV3 import vt100Parser
from scriptHandler import *
import sys, traceback

#import logging

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



class styledTextAdapter(vt100Parser):
    def __init__(self, styledTextCtrl, configuration, session):
        vt100Parser.__init__(self)
        self.ctrl = styledTextCtrl
        self.session = session
        self.configuration = configuration
        logFileNameFmtString = self.session['ansiLog']
        import logFilenameGenerator
        logFileNameString = logFilenameGenerator.logNameGen(logFileNameFmtString, \
            self.session['server'], str(session["port"]))

        self.ansiLog = file(logFileNameString, 'wb+')
        self.appLog = file(logFileNameString+'.app.log', 'w')
        self.inputLog = file(logFileNameString+'.input.log', 'w')
        #print 'logFileName'+logFileNameString
        self.connection  = None #When connecting protocol will set this value to connection
        #connectTelnet(session, self)
        self.x = 0
        self.y = 0
        self.currentCaretPos = 0
        self.currentScreenCaretPos = 0
        self.reverseColorMap = {}
        for i in range(16):
            if colorMap[colorMap.keys()[i]] != '#000000':
                self.ctrl.StyleSetSpec(i,"back:black")#add any non-style text will set style to 0
            else:
                self.ctrl.StyleSetSpec(i,"back:white")#add any non-style text will set style to 0
            #if i == 13:
            #    self.ctrl.StyleSetSpec(i,"back:white")
            self.ctrl.StyleSetForeground(i,colorMap[colorMap.keys()[i]])
            #print colorMap[colorMap.keys()[i]]
            self.reverseColorMap[colorMap[colorMap.keys()[i]]] = i
        self.width = 80
        self.height = 1
        self.logcnt = 0
        self.scrollTop = 0
        self.scrollBottom = 1
        #self.setWinSize()
        try:
            trig = self.session['triggers']
            self.scriptHandler = triggerHandler(self.sendScriptCmd, self.session)#textProcessor()
        except:
            self.scriptHandler = dummyProcessor()
        self.connected = True
        self.cursorAtEnd = True
        self.cursorAtLastLine = True
        self.EOL = '\r\n'#Currently the end of line is CRLF for styledTextCtrl
        self.playbackFile = None

        if self.configuration['global']['logDetail']:
            self.log = self.realLog
            self.debugFlag = True
            self.log('debug on')
        else:
            self.debugFlag = False

    def openScript(self, path, delay=5, prompt ='>>> '):
        self.scriptHandler.close()
        self.scriptHandler = staticScriptHandler(path, self.sendScriptCmd, delay, prompt)

    def sendScriptCmd(self, line):
        self.stringEntered(line)

    def write(self, data):#Called by telnet connector
        #logging.error('data:')
        #logging.error(data)
        for i in data:
            self.log('a:%d,%c'%(ord(i),i))
        #self.ansiLog.write('received len%d'%len(data))
        self.ansiLog.write(data)
        self.ansiParser.parseString(data)
        #print data
    
    def realLog(self, str):
        self.logcnt += 1
        if self.configuration['global']['logDetail']:
            #print '%d:%s'%(self.logcnt,str)
            print >>self.appLog,str
            
    def noLog(self, str):
        pass

    def switchDebug(self):
        print 'calling switchDebug'
        if self.debugFlag:
            self.log('end debug')
            self.log = self.noLog
            self.debugFlag = False
        else:
            self.log = self.realLog
            self.log('start debug')
            self.debugFlag = True

#-------------------------------------------------------------------------------
    
    def stringEntered(self, data):
        self.sendString(data.encode('utf8'))
        self.sendEnter()

    def sendString(self, str):
        self.checkSizeAndSendWindowSize()
        self.inputLog.write(str)
        self.connection.write(str)
        
        
    def sendEnter(self):
        self.sendString('\r\n')

#-------------------------------------------------------------------------------
    def setWinSize(self):
        visi = self.ctrl.LinesOnScreen()
        if visi != self.height:
            self.log('--------visi:%d,height:%d'%(visi,self.height))
            self.height = self.ctrl.LinesOnScreen()
            self.scrollTop = 0
            self.scrollBottom = self.height-1
            return True
        else:
            return False
        
    def checkSizeAndSendWindowSize(self):
        if self.setWinSize():
            self.connection.sendWindowSize()
        
    def char(self, event):#A char entered.
        self.log('styled:char')
        self.checkSizeAndSendWindowSize()
        if self.connection and event.GetKeyCode():
            self.connection.write(chr(event.GetKeyCode()))
            self.log('char event:%d'%event.GetKeyCode())
            
    def keyDown(self, event):
        self.log('styeld:keyDown')
        self.checkSizeAndSendWindowSize()
        #First check if the key is combined with other control key
        if event.ControlDown():
            self.connection.writeCtrlKey(event.GetKeyCode())
            #The above function will always return False. so we wont call skip here
            return
        if self.connection.writeKey(event.GetKeyCode()):
            event.Skip()#if the above code return true, then continu process the message
    
    def saveAll(self):
        self.ansiLog.close()
        self.inputLog.close()
        print 'new config----------------------------------'
        if self.playbackFile != None:
            self.playbackFile.close()
        for i in self.configuration['sessions'].keys():
            print i

        self.configuration['sessions'][self.session['sessionName']] = self.session
        if self.connected:
            self.connection.loseConnection()
        
    def rightMouseDown(self, event):
        self.ctrl.GetParent().GetParent().pasteClipboard()
    def getWidth(self):
        return self.width
    def getHeight(self):
        return self.height



#-------------------------------------------------------------------------------
    def restoreTelnetCursor(self):
        if self.ctrl.cursorUpdated:
            self.ctrl.GotoPos(self.currentCaretPos)
            self.ctrl.cursorUpdated = False

    def moveToNextLineStartAutoAppendLineEnd(self):
        self.ctrl.LineEnd()
        oldPos = self.ctrl.GetCurrentPos()
        self.ctrl.LineDown()
        #self.ctrl.CharRight()
        newPos = self.ctrl.GetCurrentPos()
        #self.log('old:%d,new:%d'%(oldPos, newPos))
        if oldPos == newPos:
            #Can not move down, append newline
            #self.log('total:%d'%self.ctrl.GetLineCount())
            self.ctrl.NewLine()
            self.ctrl.CharRight()
            #print >>self.ansiLog,'total;%d'%self.ctrl.GetLineCount()
            #Shall we move to the new line?
            self.cursorAtEnd = True
            self.cursorAtLastLine = True
        else:
            self.cursorAtEnd = False
            self.cursorAtLastLine = False
        self.currentCaretPos = self.ctrl.GetCurrentPos()

    def replaceACharWithStyle(self, ch, fg, bg):
        #self.log('styled:replaceing char')
        self.restoreTelnetCursor()

        #print >>self.ansiLog,'char:%c'%ch
        #print ch
        if ch == '\r':
            self.home()
            self.log('-----------------------write \\r')
        elif ch == '\n':
            self.lineDown(1)
        else:
            #Get the line end position
            #self.log('replacing the char')
            #self.ctrl.GotoPos(self.currentCaretPos)
            #sself.log('styled:cur pos:%d'%self.currentCaretPos)
            self.ctrl.LineEnd()
            lineEnd = self.ctrl.GetCurrentPos()
            #print >>self.ansiLog,'line end:%d'%lineEnd
            self.ctrl.GotoPos(self.currentCaretPos)
            self.ctrl.CharRightExtend()
            newPos = self.ctrl.GetCurrentPos()
            if newPos > lineEnd:
                #Get to the next line, so select the original line to end and replace
                #print >>self.ansiLog,"new pos%d"%newPos
                self.ctrl.GotoPos(self.currentCaretPos)
                self.ctrl.LineEndExtend()
                if self.cursorAtLastLine:
                    self.cursorAtEnd = True
                #print >>self.ansiLog,"end i:%d"%i
            try:
                self.ctrl.ReplaceSelection(ch)#will not change the current position?
            except:
                self.ctrl.ReplaceSelection('?')
            self.ctrl.StartStyling(self.currentCaretPos,0x1f)#Last 5 bits is the style index
            #print 'set style to:%d'%self.reverseColorMap[fg]
            #print str
            self.ctrl.SetStyling(1, self.reverseColorMap[fg])
            self.currentCaretPos = self.ctrl.GetEndStyled()
            #self.log('styled:cur pos:%d'%self.currentCaretPos)
            self.ctrl.GotoPos(self.currentCaretPos)


    def appendACharWithStyle(self, ch, fg, bg):
        #self.log('styled:appending char')
        self.restoreTelnetCursor()
        if ch == '\r':
            self.log('----------------------write \\r')
            self.home()
        elif ch == '\n':
            self.lineDown(1)
        else:
            self.ctrl.AppendText(ch)
            self.ctrl.StartStyling(self.currentCaretPos,0x1f)#Last 5 bits is the style index
            #print 'set style to:%d'%self.reverseColorMap[fg]
            #print str
            self.ctrl.SetStyling(1, self.reverseColorMap[fg])
            #self.ctrl.DocumentEnd()
            self.currentCaretPos = self.ctrl.GetEndStyled()
            self.ctrl.GotoPos(self.currentCaretPos)

    def writeChar(self, ch, fg, bg):
        if not self.cursorAtEnd:
            self.replaceACharWithStyle(ch, fg, bg)
        else:
            self.appendACharWithStyle(ch, fg, bg)
            
        self.scriptHandler.write(ch)
                
    def writeString(self, text, fg, bg):
        '''
        This function is called to write a string to view
        '''
        while not self.cursorAtEnd:
            if len(text) == 0:
                return
            self.log('styled:not end')
            c = text[0]
            self.writeChar(c, fg, bg)
            text = text[1:]
        
        self.log('styled:end')
        self.restoreTelnetCursor()
        output = self.textDecode(text)
        self.ctrl.AppendText(output)
        self.ctrl.StartStyling(self.currentCaretPos,0x1f)#Last 5 bits is the style index
        self.ctrl.SetStyling(len(output), self.reverseColorMap[fg])
        self.ctrl.DocumentEnd()
        self.log('str:%s'%text)
        #self.currentCaretPos = self.ctrl.GetEndStyled()
        self.currentCaretPos = self.ctrl.GetCurrentPos()
        
        self.scriptHandler.write(text)
#-------------------------------------------------------------------------------

    def eraseFullScreen(self):
        print 'erase full screen'
    def charMove(self, num):
        if num<0:
            self.charLeft(-num)
        else:
            self.charRight(num)
    def scrollToLast(self):
        self.log('scroll')
        last = self.ctrl.GetLineCount()
        self.ctrl.ScrollToLine(last)
        self.cursorAtEnd = False

    def eraseToEndOfScreen(self):
        self.log('before erase to end of secrren:%d'%self.currentCaretPos)
        self.restoreTelnetCursor()
        self.log('height:%d'%self.getHeight())
        self.ctrl.Home()
        self.ctrl.DelLineRight()
        for i in range(self.getHeight()-1):
            self.lineDownWithoutCursorChange(1)
            self.ctrl.Home()
            self.ctrl.DelLineRight()
        self.log('after erase to end of secrren:%d'%self.currentCaretPos)
        self.ctrl.GotoPos(self.currentCaretPos)
        self.cursorAtEnd = False

    def delRight(self):
        self.restoreTelnetCursor()
        self.ctrl.DelLineRight()
        self.currentCaretPos = self.ctrl.GetCurrentPos()
        self.cursorAtEnd = False
        
    def delLeft(self):
        self.restoreTelnetCursor()
        self.ctrl.DelLineLeft()
        self.currentCaretPos = self.ctrl.GetCurrentPos()
        self.cursorAtEnd = False
    def lineMove(self, num):
        if num<0:
            self.lineUp(-num)
        else:
            self.lineDown(num)
    def lineUp(self, num):
        self.restoreTelnetCursor()
        self.log('curpos:%d'%self.currentCaretPos)
        total = self.ctrl.GetLineCount()
        newCurLine = self.ctrl.GetCurrentLine()
        self.log('total:%d,cur:%d, up:%d'%(total,newCurLine,num))
        self.log('total line count:%d'%total)
        for i in range(num):
            self.ctrl.LineUp()
        total = self.ctrl.GetLineCount()
        newCurLine = self.ctrl.GetCurrentLine()
        self.log('total:%d,cur:%d'%(total,newCurLine))
        self.currentCaretPos = self.ctrl.GetCurrentPos()
        self.log('curpos:%d'%self.currentCaretPos)
        self.cursorAtEnd = False
        self.cursorAtLastLine = False

    def lineDownWithoutCursorChange(self, num):
        for i in range(num):
            curLine = self.ctrl.GetCurrentLine()
            self.log('curline:%d'%curLine)
            self.ctrl.LineDown()
            self.log('1 line down')
            newCurLine = self.ctrl.GetCurrentLine()
            self.log('newCur:%d'%newCurLine)
            if curLine == newCurLine:
                #Need to append new line
                for k in range(num-i):
                    self.ctrl.NewLine()
                    self.log('styled ctrl: new line added')
                    #self.ctrl.CharRight()
                return True
        return False#Last line and end of the doc

    def lineDown(self, num):
        #Move to the current position
        self.restoreTelnetCursor()
        isLast = self.lineDownWithoutCursorChange(num)
        self.currentCaretPos = self.ctrl.GetCurrentPos()
        self.cursorAtEnd = isLast
        self.cursorAtLastLine = isLast
        
    def charRight(self, num):
        self.log('calling charRight')
        self.restoreTelnetCursor()
        self.ctrl.LineEnd()
        end = self.ctrl.GetCurrentPos()
        self.ctrl.GotoPos(self.currentCaretPos)
        for i in range(num):#i started from 0
            if self.ctrl.GetCurrentPos() == end:#The last move
                self.lineEnd = True
                self.ctrl.LineEndExtend()
                #self.log('move to end of the line,i:%d,%s,%d'%(i,' '*(num-i), (num-i)))
                self.ctrl.ReplaceSelection(' '*(num-i))
                break
            self.log('not end')
            self.ctrl.CharRight()
        self.currentCaretPos = self.ctrl.GetCurrentPos()
        self.cursorAtEnd = False

    def charLeft(self, num):#Will not move left if get the first postion of the line
        self.restoreTelnetCursor()
        self.ctrl.Home()
        first = self.ctrl.GetCurrentPos()
        self.ctrl.GotoPos(self.currentCaretPos)
        for i in range(num):
            if self.ctrl.GetCurrentPos() == first:
                self.ctrl.GotoPos(self.currentCaretPos)
                self.log('move to beginning of the line')
                self.ctrl.Home()
                break
            self.ctrl.CharLeft()
        self.currentCaretPos = self.ctrl.GetCurrentPos()
        #self.scrollToLast()
        self.cursorAtEnd = False
        
    def home(self):
        self.restoreTelnetCursor()
        self.ctrl.Home()
        self.currentCaretPos = self.ctrl.GetCurrentPos()
        self.cursorAtEnd = False

    def insertLine(self):
        self.restoreTelnetCursor()
        self.log('new line added')
        self.ctrl.InsertText(self.currentCaretPos,self.EOL)
        self.currentCaretPos = self.ctrl.GetCurrentPos()

    def insertLines(self, num):
        self.restoreTelnetCursor()
        newCurLine = self.ctrl.GetCurrentLine()
        self.log('before insert:%d'%newCurLine)
        for i in range(num):
            self.log('new line added')
            self.ctrl.InsertText(self.currentCaretPos,self.EOL)
        newCurLine = self.ctrl.GetCurrentLine()
        self.log('before insert:%d'%newCurLine)
        self.currentCaretPos = self.ctrl.GetCurrentPos()

    def clearLine(self):
        self.restoreTelnetCursor()
        self.ctrl.DelLineRight()
        self.ctrl.Home()
        lineBegin = self.ctrl.GetCurrentPos()
        #self.x = self.currentCaretPos - lineBegin
        self.ctrl.LineEndExtend()
        self.ctrl.ReplaceSelection('')
        self.currentCaretPos = self.ctrl.GetCurrentPos()
        self.cursorAtEnd = False

    def delLine(self):
        self.removeLine()
        
    def removeLines(self, num):
        self.restoreTelnetCursor()
        for i in range(num):
            self.removeLineWithoutCursorUpdate()
        self.currentCaretPos = self.ctrl.GetCurrentPos()
        self.cursorAtEnd = False
        
    def removeLineWithoutCursorUpdate(self):
        self.ctrl.LineEnd()
        self.ctrl.HomeExtend()
        self.ctrl.CharLeftExtend()
        self.ctrl.ReplaceSelection('')
        
    def removeLine(self):
        self.removeLines(1)
        
    def deleteLeft(self, num):
        self.restoreTelnetCursor()
        self.ctrl.Home()
        first = self.ctrl.GetCurrentPos()
        self.ctrl.GotoPos(self.currentCaretPos)
        for i in range(num):
            if self.ctrl.GetCurrentPos() == first:
                self.ctrl.GotoPos(self.currentCaretPos)
                self.log('move to beginning of the line')
                self.ctrl.HomeExtend()
                break
            self.ctrl.CharLeftExtend()
        self.ctrl.ReplaceSelection('')
        self.currentCaretPos = self.ctrl.GetCurrentPos()
        self.cursorAtEnd = False
        
    def deleteRight(self, num):
        self.restoreTelnetCursor()
        self.ctrl.LineEnd()
        lineEnd = self.ctrl.GetCurrentPos()
        #print >>self.ansiLog,'line end:%d'%lineEnd
        self.ctrl.GotoPos(self.currentCaretPos)
        for i in range(num):
            newPos = self.ctrl.GetCurrentPos()
            if newPos == lineEnd:
                #Get to the next line, so select the original line to end and replace
                #print >>self.ansiLog,"new pos%d"%newPos
                self.ctrl.GotoPos(self.currentCaretPos)
                self.ctrl.LineEndExtend()
                break
                #print >>self.ansiLog,"end i:%d"%i
            self.ctrl.CharRightExtend()
        self.ctrl.ReplaceSelection('')
        self.currentCaretPos = self.ctrl.GetCurrentPos()
        self.cursorAtEnd = False
#-------------------------------------------------------------------------------

    def runScript(self):
        #Select a file
        from scriptSelectDialog import chooseScript
        dlg = chooseScript(self.ctrl)
        dlg.initHist(self.session)
        dlg.ShowModal()
        path = dlg.GetPath()
        print '---------------------%s'%path

        #print 'You selected file is %s:' % (path)
        if path:#open a file
            self.openScript(path,dlg.delay, dlg.pattern)
        dlg.Destroy()
    def play(self, path):
        self.playbackFile = open(path,'rb')
    
    def step(self, num = 10):
        self.write(self.playbackFile.read(num))
    

    def clientConnectionLost(self, reason):
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
        self.ctrl.frame.title(self.session['sessionName']+"client connection lost" + str(reason))
    def clientConnectionFailed(self, reason):
        self.connected = False
        self.ctrl.frame.title(self.session['sessionName']+"client connection failed" + str(reason))

