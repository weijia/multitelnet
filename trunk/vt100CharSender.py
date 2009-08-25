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
    self.behaviour = xtermBehaviour()
    
  def sendData(self, d):
    print 'sendData called'
    for i in d:
      c = self.behaviour.translateSpecialChar(i)
      if c == None:
        #Normal key, send itself
        self._write(i)
      else:
        #Special key, send translated char
        '''
        if len(c) > 1:
          o = ord(c[0])
        else:
          o = ord(c)
        print 'sending %d'%o
        '''
        self._write(c)

  def sendKeyWithCtrl(self, key):#Key should only be 'A'-'Z'
    #"CTRL" key pressed with key.
    sendKey = key-ord('A')+1#'A' will send 1 to server
    self._write(chr(sendKey))
    return False#tell the window msg hendler do not process the message again
    
#------------------------------------------------------------------------------------
#The following codes should not be called
  def setTermType(self, termType):
    self.behaviour = termTypeBehaviourMapping[termType]()
    self.log('using new term type')

  def crCharReceived(self):
    self.behaviour.translateReceivedSpecChar(self, '\r')

  def newLineCharReceived(self):
    self.behaviour.translateReceivedSpecChar(self, '\n')


  def _write(self, data):
    #print '_writing:',data,ord(data[0])
    #Write data to server through connection
    self.inputLog.write(data)
    #print self.connection
    self.connection.sendApplicationData(data)#Connection is set in appTelnetTransport init function
