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
    
def findPattern(line, patternDict):
  for i in patternDict.keys():
    if line.find(i) != -1:
      yield i



class triggerHandler(textHandlerLineProducer):
  def __init__(self, sess, delay = 5):
    self.sess = sess
    textHandlerLineProducer.__init__(self, delay)
  def linesReceived(self, lines):
    #print 'lineReceived', lines
    for i in lines:
      #Check auto command send
      for j in findPattern(i, self.sess.trgs):
        if self.sess.trgs[j]['enabled']:
          self.sess.send(self.sess.trgs[j]['action'])
      #Check callback
      for j in findPattern(i, self.sess.callbackTrgs):
        if self.sess.trgs[j]['enabled']:
          self.sess.trgs[j]['callback'](j)


#We should clean all buffer after every command received. It is to say we'll keep a cache of text so no output will be ignored due to the later arrival of the next command.
class captureHandler:
  def __init__(self, sess):
    self.sess = sess
    self.capture = False
    self.data = []
  def handleData(self, text):#This function will be called by other class to send data to it
    #print 'capture line',lines
    if self.capture:
      #print 'handle data called in delay handle base', text
      self.data.append(text)#No text removed

  def getCaptured(self):
    res = self.data
    self.data = []
    return ''.join(res)
    
  def enableCapture(self, flag = True):
    if flag:
      self.capture = True
    else:
      self.capture = False
  def clean(self):
    self.data = []
      
class waitHandler(textHandlerLineProducer):
  '''
  If there is no trigger enabled, shall session object cache the output? As the wait function will be called
  later after issue the command, there is possibility that the wait function will be called after the output
  of a command is already outputted. As the above case may be a problem for wait function, we may combine the
  send and wait to 1 function?
  '''
  def __init__(self, sess, delay = 5):
    self.lines = []
    self.inAWait = False
    self.sess = sess
    textHandlerLineProducer.__init__(self, delay)
  def linesReceived(self, lines):
    #print 'wait handler: line received:',lines
    if self.inAWait:
      #We are already waiting someting, So find it now.
      self.checkLines(lines)
    else:
      print 'wait handler: save lines'
      self.lines.extend(lines)
  def checkLines(self, lines):
    print 'checking lines'
    for i in lines:
      for j in findPattern(i, self.sess.waitPattern):
        self.sess.waitPattern[j]['callback'](j)
        self.inAWait = False
        return

  def startWait(self):
    self.inAWait = True
    self.checkLines(self.lines)

  def stopWait(self):
    self.inAWait = False
  def clean(self):
    #print 'before clean:',self.lines
    self.lines = []
    #print 'cleaned:',self.lines
    
class session(object):
  def __init__(self):
    self.server = None
    self.port = None
    self.timeoutHandler = None#Will not be saved to configuration file
    self.callbackTrgs = {}
    self.trgs = {}#Will not be saved to configuration file
    self.waitPattern = {}
  def connectToServer(self, server, port, isSsh = False, forwardConnection = False):
    self.server = server
    self.port = port
    self.sess = wxConsoleApp.consoleMan.openTmpSession(server, port, self.trgs, self.timeoutHandler)
    self.textHandler = triggerHandler(self, 1)
    self.captureHandler = captureHandler(self)
    self.waitHandler = waitHandler(self, 1)
    self.sess.addDataHandler(self.textHandler)
    self.sess.addDataHandler(self.captureHandler)
    self.sess.addDataHandler(self.waitHandler)
  def addTrigger(self, pattern, autoSendData):
    self.trgs[pattern] = {'action':autoSendData,'enabled':True}
    print 'adding:',pattern, autoSendData
    
  def addCallbackTrigger(self, pattern, callback):
    self.callbackTrgs[pattern] = {'callback':callback,'enabled':True}
    print 'adding:',pattern, callback
  def callbackTriggerOff(self, pattern):
    self.callbackTrgs[pattern]['enabled'] = False
    
  def send(self, data):
    self.flushAll()
    self.waitHandler.clean()#Clean as we only need to check waiting pattern after command is sent
    self.sess.sendData(data)
  def disableAllCallback(self):
    for i in self.trgs.keys():
      self.trgs[i]['enabled'] = False
    for i in self.callbackTrgs.keys():
      self.callbackTrgs[i]['enabled'] = False
  def triggerOff(self, pattern):
    self.trgs[pattern]['enabled'] = False
  def flushAll(self):
    #self.captureHandler.flushData()
    self.sess.flushData()
  def startCapture(self):
    print 'start capture'
    self.flushAll()
    self.captureHandler.enableCapture()
    
  def endCapture(self):
    print 'end capture'
    self.flushAll()
    self.captureHandler.enableCapture(False)
    return self.captureHandler.getCaptured()
  def wait(self, pattern, callback):
    self.waitPattern = {}
    self.waitPattern[pattern] = {'callback':callback,'enabled':True}
    print 'adding wait:',pattern, callback
    self.waitHandler.startWait()
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

