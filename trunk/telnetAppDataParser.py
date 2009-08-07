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
    
class delayOutputParser(telnetAppDataParser):
  '''
  Only update terminal data after 0.5 seconds, so function calls will be minimized
  '''
  def __init__(self, styledTextCtrl, configuration, session):
    self.dataList = []
    telnetAppDataParser.__init__(self, styledTextCtrl, configuration, session)

  def dataReceived(self, data):
    self.dataList.append(data)
    from twisted.internet import reactor
    reactor.callLater(0.5, self.delayedParser)

  def delayedParser(self):
    d = ''.join(self.dataList)
    self.adapter.dataReceived(d)
    dataList = []