
class logSwitcher:
  def __init__(self, configuration, session):
    self.session = session
    self.configuration = configuration
    logFileNameFmtString = self.session['ansiLog']
    import logFilenameGenerator
    
    logFileNameString = logFilenameGenerator.logNameGen(logFileNameFmtString, \
        self.session['server'], str(session["port"]))
    self.ansiLogFilename = logFileNameString
    self.ansiLog = file(logFileNameString, 'wb+')
    self.appLog = file(logFileNameString+'.app.log', 'w')
    self.inputLog = file(logFileNameString+'.input.log', 'w')
    #print 'logFileName'+logFileNameString
    self.configuration['global']['logDetail'] = False
    if self.configuration['global']['logDetail']:
        self.log = self.realLog
        self.debugFlag = True
        self.log('debug on')
    else:
        self.debugFlag = False
    def openLogFile(self):
        import os
        print self.ansiLogFilename
        os.spawnv(os.P_NOWAIT, "D:/Program Files/Programmers Notepad/pn.exe", ("\"D:/Program Files/Programmers Notepad/pn.exe\"",self.ansiLogFilename))
    
    def realLog(self, str):
        self.logcnt += 1
        if self.configuration['global']['logDetail']:
            print '%d:%s'%(self.logcnt,str)
            print >>self.appLog,str
            
    def noLog(self, str):
        pass

    def switchDebug(self):
        print 'calling switchDebug'
        if self.debugFlag:
            print 'end debug'
            self.log('end debug')
            self.debugFlag = False
            self.log = self.noLog
            #print self.log
        else:
            print 'start debug'
            self.configuration['global']['logDetail'] = True
            self.log = self.realLog
            self.debugFlag = True
            self.log('start debug')
            #print self.log
