
class logSwitcher:
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
