import re

class dummyProcessor:
    def __init__(self, path = None, notifObj = None, delay=5, prompt ='>>> '):
        pass
    def write(self, ch):
        pass
    def close(self):
        pass



class timeoutAndLineFeedHandler:
    def __init__(self, notifObj, delay=5):
        self.maxTimeout = delay#This is based on the timerPeriod?
        self.maxTimeoutCnt = delay
        self.callScriptDelay = 1
        self.callingScript = False
        self.newDataReceivedCnt = 0
        self.lastDataChecked = 0
        self.lastOutputLine = ''
        self.lastDataReceivedCnt = 0
        self.timerPeriod = 2#Seconds
        self.startAutoScriptTimer()
        self.notifObj = notifObj

    def complexSplit(self, str, splitChars):
        result = str.split(splitChars[0])
        tmpResult = []
        for i in splitChars[1:]:
            for j in result:
                tmpResult.extend(j.split(i))
            result = tmpResult
            tmpResult = []
        return result
    
    def startAutoScriptTimer(self):
        from twisted.internet import reactor
        reactor.callLater(self.timerPeriod, self.timerCallback)
    '''
    def maxTimeoutCallback(self):
        #This function is called every self.maxTimeout seconds
        print 'timeout called'
        if self.newDataReceivedCnt == self.lastDataReceivedCnt:
            #For self.maxTimeout seconds, we havent receive any data, call callStaticScript
            self.timeoutAction()
        #Update the timeout cnt
        self.lastDataReceivedCnt = self.newDataReceivedCnt
    '''
    def timerCallback(self):
        if self.newDataReceivedCnt == self.lastDataReceivedCnt:
            #For pattern match, we havent receive any data, call callStaticScript
            self.maxTimeoutCnt -= 1
            if self.maxTimeoutCnt < 1:
                self.timeoutAction()
                self.maxTimeoutCnt = self.maxTimeout
        else:
            self.lastDataReceivedCnt = self.newDataReceivedCnt
        #Put here below so it will not be too long to handle the terminal output
        if self.lastDataChecked != self.newDataReceivedCnt:
            self.lastDataChecked = self.newDataReceivedCnt
            self.periodicallyCheckTerminalOutput()
        self.startAutoScriptTimer()

    def write(self, ch):
        #-------------------------------------------------------------------------------
        #The following codes is for trigger use, here seems only 1 char will be passed here
        #print 'write %c'%ch
        self.newDataReceivedCnt +=1
        self.lastOutputLine += ch
        #print self.lastOutputLine
        
    def periodicallyCheckTerminalOutput(self):
        lines = self.complexSplit(self.lastOutputLine, '\r\n')
        partNum = len(lines) - 1
        self.lastOutputLine = lines[partNum]
        self.linesReceived(lines)
    
    
    def delayCallFunc(self, func):
        #This function will add the function to callback list
        if self.callingScript:
            print 'calling script but another call request received'
            return
        self.callingScript = True
        from twisted.internet import reactor
        reactor.callLater(self.callScriptDelay, func)
        
    def delaySendCmd(self, cmd):
        self.cmd = cmd
        self.delayCallFunc(self.sendCmdCallback)
        
    def sendCmdCallback(self):
        self.callingScript = False
        self.notifObj(self.cmd)
        
    def linesReceived(self, lines):
        pass
    
    def close(self):
        pass
    def timeoutAction(self):
        pass

class dummyTimeoutAndLineFeedHandler(timeoutAndLineFeedHandler):
    def linesReceived(self, lines):
        pass
    def close(self):
        pass
    def timeoutAction(self):
        pass
#-------------------------------------------------------------------------------

class staticScriptHandler(timeoutAndLineFeedHandler):
    def __init__(self, path, notifObj, delay=5, prompt ='>>> '):
        print 'loading%s'%path
        self.scriptLines = open(path,'r').readlines()
        '''
        for i in self.scriptLines:
            print i
        '''
        self.scriptLoaded = True
        self.curScriptLineNum = 0
        self.promptString = prompt
        self.promptString = '>>> '
        self.curScriptLineNum = 0
        timeoutAndLineFeedHandler.__init__(self, delay, notifObj)
        
    def callStaticScript(self):
        print 'script called'
        self.callingScript = False
        #This function will be called in 2 different condition
        #1. an predefined prompt string is captured on terminal
        #2. an predefined time after the last char received.
        #Remove \r\n
        while True:
            try:
                #print 'current script line:%d'%self.curScriptLineNum
                '''
                for i in self.scriptLines:
                    print i
                '''
                line = self.scriptLines[self.curScriptLineNum]                
            except IndexError:
                self.scriptLoaded = False
                print 'no more script lines'
                return
            if line != '':
                break
        line = line.replace('\r','').replace('\n','')
        #print 'input: %s'%line
        self.notifObj(line)
        self.curScriptLineNum +=1
        
    def linesReceived(self, lines):
        partNum = len(lines) - 1
        lastLine = lines[partNum]
        #print 'the final output line'
        #print self.lastOutputLine
        last = lastLine.rfind(self.promptString)
        if last != -1:
            #Find the string. Check if it is the last part?
            #print last
            if lastLine[last:] == self.promptString:
                #The end match. call script? Or wait and call?
                print 'match prompt'
                self.delayCallFunc(self.callStaticScript)
                
    def timeoutAction(self):
        self.delayCallFunc(self.callStaticScript)

class triggerHandler(timeoutAndLineFeedHandler):
    def __init__(self, notifObj, session, delay=25):
        self.session = session
        timeoutAndLineFeedHandler.__init__(self, notifObj, delay)
    
    def linesReceived(self, lines):
        triggers = self.session['triggers']
        for i in lines:
            for t in triggers.keys():
                if re.compile(t).search(i):
                    #Match
                    print 'match:term:%s,patt:%s'%(i,t)
                    action = triggers[t].doAction(self.session)
                    if action != None:
                        if type(action) == 'list':
                            for i in action:
                                print 'cmd:%s'%action
                                self.delaySendCmd(action)
                        else:
                            print 'cmd:%s'%action
                            self.delaySendCmd(action)
                    else:
                        print 'cmd is None'
        
    def timeoutAction(self):
        #self.delaySendCmd('\r\n')
        try:
            act = self.session['timeoutHandler']
            if isinstance(act, str):
                self.delaySendCmd(act)
                print 'cmd str will be sent'
            else:
                cmd = act(self.session)
                if cmd != None:
                    self.delaySendCmd(cmd)
                    print 'act func called'
        except KeyError:
            print 'no timeoutHandler provided in trigger handler'
        print 'timeout action'
        pass