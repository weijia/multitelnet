import wxConsoleApp
from textHandler import *
logPath = 'd:/'


localSession = {'sessionName':'localhost:2111','server':'localhost','port':2111,'cmdHist':[],
                'rightMouseDown':"copyToClip",
                'ansiLogName':'%(server)s_%(port)s_%(time)s_ansi.log',
                'ansiLog':logPath+'%(server)s_%(port)s_%(time)s_ansi.log',
                'charLog':logPath+'char.log',
                'baseDir':'d:/tmp/','cmdHistState':{},'sshFlag':False}

class sessionManager:
  def createSession(self):
    return session()


class triggerHandler(textHandlerLineProducer):
  def __init__(self, sess):
    self.sess = sess
    textHandlerLineProducer.__init__(self)
  def linesReceived(self, lines):
    #print 'lineReceived', lines
    for i in lines:
      #print 'rcvd',i
      for j in self.sess.trgs.keys():
        #print 'chking',j
        if self.sess.trgs[j]['enabled']:
          if i.find(j) != -1:
            self.sess.send(self.sess.trgs[j]['action'])
    
    
class session(object):
  def __init__(self):
    self.server = None
    self.port = None
    self.trgs = {}#Will not be saved to configuration file
    self.timeoutHandler = None#Will not be saved to configuration file
  def connectToServer(self, server, port, isSsh = False, forwardConnection = False):
    self.server = server
    self.port = port
    self.sess = wxConsoleApp.consoleMan.openTmpSession(server, port, self.trgs, self.timeoutHandler)
    self.textHandler = triggerHandler(self)
    self.sess.addDataHandler(self.textHandler)
  def addTrigger(self, pattern, autoSendData):
    self.trgs[pattern] = {'action':autoSendData,'enabled':True}
    print 'adding:',pattern, autoSendData
  def addCallbackTrigger(self, pattern, callbackServer = 'localhost'):
    pass
  def send(self, data):
    self.sess.sendData(data)
  def triggerOff(self, pattern):
    self.trgs[pattern]['enabled'] = False
  #override the assign operator
  def __setattr__(self, name, value):
    if name == 't':
      #It is setting triggers
      print 'trigger:',name, value
      self.addTrigger(value[0], value[1])
    elif name == 'tmo':
      #Set timeout handler
      self.timeoutHandler = value
    elif name == 's':#Send
      print 'sending',value
      self.send(value)
    elif name == 'w':#wait for something
      self.addSingleTrigger(value)
    elif name == 'td':#disable trigger
      self.triggerOff(value)
    else:
      object.__setattr__(self, name, value)

