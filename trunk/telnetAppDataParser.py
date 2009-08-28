from termCtrl import *

class telnetAppDataParser:
  def __init__(self, configuration, session):
    self.terminalWnd = termWin(None)
    self.terminalWnd.initSession(configuration, session, self)
    self.terminalWnd.Show()
    self.adapter = self.terminalWnd.adapter
    
  def dataReceived(self, data):#Called by telnet connector
    self.adapter.dataReceived(data)
    
  def onDisconnected(self, reason):
    self.terminalWnd.onDisconnected(reason)
    
  def setConnection(self, connection):
    self.adapter.connection = connection
    
  def getPassword(self):
    self.getPassDefer = defer.Deferred()
    self.getPassFlag = True
    return self.getPassDefer
  def setTermType(self, termtype):
    pass
  def addDataHandler(self, handler):
    self.adapter.addDataHandler(handler)
  def sendData(self, data):
    self.adapter.sendData(data)
    
class delayOutputParser(telnetAppDataParser):
  '''
  Only update terminal data after 0.5 seconds, so function calls will be minimized
  '''
  def __init__(self, configuration, session, delayTime = 0.2):
    self.dataList = []
    self.session = session
    telnetAppDataParser.__init__(self, configuration, session)
    from twisted.internet import reactor
    self.scheduled = reactor.callLater(999999, self.delayedParser)
    self.delayTime = delayTime
    
    #Data log for connection
    import logFilenameGenerator
    logFileNameFmtString = self.session['ansiLog']
    logFileNameString = logFilenameGenerator.logNameGen(logFileNameFmtString, \
        self.session['server'], str(session["port"]))
    self.ansiLogFilename = logFileNameString
    self.ansiLog = file(logFileNameString, 'wb+')
    
  def dataReceived(self, data):
    #Write the connection data
    self.ansiLog.write(data)
    
    #Send data to view
    self.dataList.append(data)
    from twisted.internet import reactor
    if self.scheduled.active():
      self.scheduled.cancel()
    self.scheduled = reactor.callLater(self.delayTime, self.delayedParser)

  def delayedParser(self):
    d = ''.join(self.dataList)
    self.adapter.dataReceived(d)
    self.dataList = []
  def flushData(self):
    self.delayedParser()