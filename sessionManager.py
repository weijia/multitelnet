#import wxConsoleApp
from session import *
#from multiConsoleManagerV2 import multiConsoleManager
from termCtrl import *
from forwardServerManager import *
from viewManager import *
from clientManager import *
from mtelXmlRpcServer import *

class sessionManager:
  def __init__(self, toolboxFrame, config):
    self.toolbox = toolboxFrame
    self.config = config
    self.childs = []
    self.sessionList = {}
    #self.server.startSimpleServer(1234)
    self.vwMngr = viewManager(self.config)
    self.fwdSvrMngr = forwardServerManager(self.vwMngr, self.config)
    self.clientMngr = clientManager(self.vwMngr, self.config)
    self.startXmlRpcServer()
    
  def startXmlRpcServer(self):
    from twisted.internet import reactor
    r = mtelXmlRpcServer(self)
    reactor.listenTCP(8889, server.Site(r))
        
  def createSession(self):
    import uuid
    u = str(uuid.uuid4())
    self.sessionList[u] = session(self)
    return u
    
  #--------------------------------------------------------------------------------------------------------------------------------------------------------
  #The following functions can be called outside of this class.
  def openTmpSession(self, sess):
    import uuid
    sess.sessCfg['sessionName'] = sess.sessCfg['server']+':'+str(sess.sessCfg['port'])+'-'+str(uuid.uuid4())+'-temp-session'
    import os
    #sess.sessCfg['triggers'] = triggers
    sess.sessCfg['ansiLog'] = os.path.join(sess.sessCfg['baseDir'], sess.sessCfg['ansiLogName'])
    '''
    if timeoutHandler is None:
        print 'handler provided'
        sess.sessCfg['timeoutHandler'] = timeoutHandler 
    '''
    return self.openSession(sess)
      
  def openFwdServer(self, sessConfigData):
    sess = self.sessionList[self.createSession()]
    sess.sessCfg = sessConfigData
    return self.fwdSvrMngr.createForwardServer(sess)

  def openSessionWithCfg(self, sessConfigData):
    sess = self.sessionList[self.createSession()]
    sess.sessCfg = sessConfigData
    child = self.clientMngr.createTelnetClient(sess)
    self.childs.append(child)
    return child#return the opened session
  def openSession(self, sess):
    child = self.clientMngr.createTelnetClient(sess)
    self.childs.append(child)
    return child#return the opened session
    
  def openPlayBackSession(self, sessConfigData):
    sess = self.sessionList[self.createSession()]
    sess.sessCfg = sessConfigData
    child = self.clientMngr.createPlaybackClient(sess)
    self.childs.append(child)
    return child#return the opened session

  def closeAll(self):
    for i in self.childs:
      try:
        i.Close()
      except:
        pass


  '''
  def newSession(self):
      self.toolbox.Show()
  def hello(self):
      pass
  '''

