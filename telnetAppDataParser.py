from termCtrl import *

class telnetAppDataParser:
  def __init__(self, configuration, sess):
    self.terminalWnd = termWin(None)
    self.terminalWnd.initSession(configuration, sess.sessCfg, self)
    self.terminalWnd.Show()
    self.adapter = self.terminalWnd.adapter
  def runScript(self, p):
    self.sess.runScript(p)
    
  def getTermWin(self):
    return terminalWnd
    
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
  def __init__(self, configuration, sess, delayTime = 0.2):
    self.dataList = []
    self.sess = sess
    telnetAppDataParser.__init__(self, configuration, sess)
    from twisted.internet import reactor
    self.scheduled = reactor.callLater(999999, self.delayedParser)
    self.delayTime = delayTime
    
    #Data log for connection
    import logFilenameGenerator
    logFileNameFmtString = self.sess.sessCfg['ansiLog']
    logFileNameString = logFilenameGenerator.logNameGen(logFileNameFmtString, \
        self.sess.sessCfg['server'], str(self.sess.sessCfg["port"]))
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