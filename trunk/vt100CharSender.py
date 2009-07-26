from vt100ParserV3 import *
from logSys import *
from telnetConnector import *
from vt100DefaultBehaviour import *

#Not fully understood
vt100TermKeyComplexMapping = {
    #input  telnetOption    enabledValue    disabledValue
    ptKey_cr:     [0x22,          ['\r\n',        '\r'+chr(0)]]#Enter
}

termTypeBehaviourMapping = {'XTERM':xtermBehaviour
}


class terminalSendCharBase(vt100Parser):
  def __init__(self, *argv):
    vt100Parser.__init__(self, *argv)
    self.behaviour = vt100DefaultBehaviour()
  def sendString(self, s):
    self.checkSizeAndSendWindowSize()
    print 'sending:',s
    self.inputLog.write(s)
    self.send(s)


  def writeCtrlWithKey(self, key):#Key should only be 'A'-'Z'
    #"CTRL" key pressed with key.
    sendKey = key-ord('A')+1#'A' will send 1 to server
    if self.connection.getOptionState(chr(01)).him.state == 'no':
        #Server will not echo, so we need to echo, it should be ^A etc.
        self.view.log('will echo')
        if key>255:
            self.view.log('out of 256%d'%key)
        else:
            self.send('^'+chr(key))
    self._write(chr(sendKey))
    return False#tell the window msg hendler do not process the message again

  def writeSpecialKey(self, ch):
    self.log('terminalSendCharBase: writing %d'%ch)
    snd = self.behaviour.translateSpecialChar(ch)
    if snd is None:
      #The char is not processed, return True so it will be further processed.
      self.log('not special char')
      return True
    else:
      self.send(snd)
      return False
  
  
  def setTermType(self, termType):
    self.behaviour = termTypeBehaviourMapping[termType]()
    self.log('using new term type')
    
  def crCharReceived(self):
    self.behaviour.translateReceivedSpecChar(self, '\r')

  def newLineCharReceived(self):
    self.behaviour.translateReceivedSpecChar(self, '\n')
    
  def send(self, data):
    s = self.connection.getOptionState(chr(01))#ECHO?
    if s.him.state == 'no':
        #Server will not echo, so we need to echo
        #cl('our echo state:'+str(s.us.state))
        print 'server echo state:'+s.him.state
        self.write(data)
    #print 'our echo state:'+s.us.state
    self._write(data)
  def _write(self, data):
    #print '_writing:',data,ord(data[0])
    #Write data to server through connection
    self.connection._write(data)
