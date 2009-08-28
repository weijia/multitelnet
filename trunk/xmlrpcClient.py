import xmlrpclib
#Port 80 is the default
'''
server = xmlrpclib.ServerProxy("http://localhost:8889")
currentTimeObj = server.helloworld()
print currentTimeObj
'''
from communication import *
import time



class remoteSession(object):
  def __init__(self):
    self.shortcutMapping = {'ww': self.waitForCallback,
      'w':self.waitForPattern,
      'c':self.connect,
      'tc':self.addTriggerCallback,
      'td':self.triggerOff,
      's':self.send,
      'tcd':self.callbackTriggerOff,
      'tmo':self.timeoutHandler,
      't':self.addTrigger,
      'sc':self.startCapture
    }

    self.serverAddr = 'localhost'
    self.port = 9527
    self.queueAddr = (self.serverAddr, self.port)
    #checkServer(self.queueAddr)
    startServer(self.queueAddr)
    self.server = xmlrpclib.ServerProxy("http://localhost:8889")
    self.sessid = self.server.sess()
    print self.sessid
  def __del__(self):
    print 'quitting, disable all triggers'
    self.server.disconnectRemote(self.sessid)
    self.server.disableAllCallback(self.sessid)
    self.server.ecp(self.sessid)
    
  def waitForPattern(self, pattern):
    print 'wait for pattern', pattern
    self.server.w(self.sessid, pattern, self.serverAddr, self.port)
    self.waitForCallback()
    
  def connect(self, value):
    self.server.con(self.sessid, value[0], value[1])
    
  def send(self, data):
    self.server.s(self.sessid, data)
    
  def addTrigger(self, value):
    pattern = value[0]
    autoSendCmd = value[1]
    self.server.t(self.sessid, pattern, autoSendCmd)
    
  def addTriggerCallback(self, pattern):
    print pattern, self.sessid, self.server, self.port
    self.server.tc(self.sessid, pattern, self.serverAddr, self.port)
    
  def waitForCallback(self):
    receive(self.queueAddr)
    
  def callbackTriggerOff(self, pattern):
    self.server.tcd(self.sessid, pattern)
  def triggerOff(self, pattern):
    self.server.td(self.sessid, pattern)
  
  def timeoutHandler(self, value):
    pass
  def startCapture(self, value):
    self.server.scp(self.sessid)
  def ec(self):
    return self.endCapture(None)
  def endCapture(self, value):
    return self.server.ecp(self.sessid)
  def __setattr__(self, name, value):
    try:
      if self.shortcutMapping.has_key(name):
        self.shortcutMapping[name](value)
        return
    except:
      pass

    object.__setattr__(self, name, value)

class rmtS(remoteSession):
  pass
      
def main():
  s = remoteSession()
  #time.sleep(3)
  s.c = 'localhost', 2111
  s.w = 'Username:'
  #time.sleep(3)
  s.s = 'admin\r'
  #time.sleep(3)
  s.w = 'Password:'
  s.s = 'wwj\r'
  
  s.w = '\'gM\''
  #time.sleep(3)
  s.sc = 0#Start capture
  s.s = 'dir(gM)\r'
  #time.sleep(10)
  s.w = '>>>'
  print s.ec()#End capture
  import time
  #time.sleep(30)
  
if __name__ == '__main__':
    main()