from twisted.internet.protocol import ClientFactory
'''
from twisted.conch.telnet import Telnet
from twisted.conch.telnet import TelnetProtocol
from twisted.conch.telnet import TelnetTransport
from twisted.conch.telnet import NAWS
'''
from telnet import Telnet
from telnet import TelnetProtocol
from telnet import TelnetTransport
from telnet import NAWS

from logSys import *
'''
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='d:\\log.txt',
                    filemode='w')
'''

class optionLogTelnetProtocol(TelnetProtocol):
    def __init__(self, protocol):
        self.protocol = protocol
        self.negFlag = False
        
    def unhandledCommand(self, command, argument):
        try:
            cl('unhandledCmd:'+command + argument)
        except:
            cl('unhandledCmd')

    def unhandledSubnegotiation(self, command, bytes):
        cl('unhandledNeg:',command, bytes)

    def enableLocal(self, option):
        cl('enable local:',ord(option), option)
        if None != self.negFlag :
            self.negFlag = True
        if option == chr(24):
            cl('enableLocal termtype 24')
            #Return True if termtype will be enabled.
            return True
            #self.protocol.sendTermType()
        elif option == chr(01):#ECHO
            cl('enableLocal echo')
            return True
        elif option == NAWS:
            #self.protocol.will(option)
            return True
        #cl('enableLocal:'+ option)
        #self.sendInitialNeg()#We send initial neg only we received neg command so we are sure the other part support telnet protocol

    def enableRemote(self, option):
        #The remote here is said from the server side, so it's server ask client to support echo?
        #Answser is no. Server is offer to let himself enable ECHO
        if option == chr(01):#ECHO
            cl('enableRemote echo')
            #We are echoing so ask server do not echo
            return True
        cl('enableRemote:'+ option,ord(option))

    def disableLocal(self, option):
        cl('disableLocal:'+ option,ord(option))

    def disableRemote(self, option):
        cl('disableRemote:'+ option,ord(option))




class appTelnetTransport(TelnetTransport):
    def __init__(self, view):
        self.view = view
        #view.connection = self
        self.view.setConnection(self)
        #The following will be used by Telnet instance
        self.protocol = optionLogTelnetProtocol(self)
        Telnet.__init__(self)
        self.negotiationMap[chr(24)] = self.sendTermType
        self.negotiationMap[chr(0x1f)] = self.sendWindowSize
        
    '''
    def connectionMade(self):
        #Called after connected
        
        #Call original function
        TelnetTransport.connectionMade(self)
    '''

    def applicationDataReceived(self, data):
        self.view.dataReceived(data)
        #print data

    '''
    #We can handle option in TelnetProtocol, if we return True, it means we support the option
    def getOptionState(self, option):
        class _OptionState:
            class _Perspective:
                def __init__(self, state = 'no', neg = False, onRes = None)
                    self.state = state
                    self.negotiating = neg
                    self.onResult = onRes

                def __str__(self):
                    return self.state + ('*' * self.negotiating)

            def __init__(self):
                self.us = self._Perspective()
                self.him = self._Perspective()
                
            def __repr__(self):
                return '<_OptionState us=%s him=%s>' % (self.us, self.him)

        if option == chr(24):
            #self.will(option)
            cl('neo 24')
        elif option == chr(01):
            cl('echo')
            #self.protocol.will(option)
        elif option == NAWS:
            #self.protocol.will(option)
            value = self._OptionState()
            value.us = self._Perspective()
            value.him = self._Perspective()
            return self.options.setdefault(opt, )
        
        cl('enableLocal:'+ option)
        return TelnetTransport.getOptionState(self, option)
    '''
    
    def sendTermType(self, bytes):
        #self.will(chr(24))#need not since it is acked already
        #The server seems do not reply for the above command, send it manually
        #Write termtype to server
        self.requestNegotiation('termtype', chr(24)+chr(0)+'XTERM')
        self.termType = 'XTERM'
        self.view.setTermType('XTERM')
        #self.sendWindowSize()
        
    def sendWindowSize(self):
        #self.will(chr(24))#need not since it is acked already
        #The server seems do not reply for the above command, send it manually
        #Write termtype to server
        self.requestNegotiation('windSize', chr(0x1f)+\
            chr((self.view.getWidth()&0xff00)>>8)+chr((self.view.getWidth()&0xff))+\
            chr((self.view.getHeight()&0xff00)>>8)+chr((self.view.getHeight()&0xff))
            )
        print 'winsize width:%d'%self.view.getWidth()
        print 'winsize height:%d'%self.view.getHeight()

    '''
    def callbackfunc(self, option):
        cl('callback called')
        self.will(option)
    '''



class telnetClient(appTelnetTransport):
  def sendApplicationData (self, data) :
    #Send the data directly
    s = self.getOptionState(chr(01))#ECHO?
    if s.him.state == 'no':
        #Server will not echo, so we need to echo
        #cl('our echo state:'+str(s.us.state))
        #print 'server echo state:'+s.him.state
        self.view.dataReceived(data)
    #print 'our echo state:'+s.us.state

    self._write(data)

class dummyConnection:
    def loseConnection(self):
        pass



class telnetForwardClient (telnetClient) :
  def __init__(self, view, fwd):
    telnetClient.__init__(self, view)
    self.fwd = fwd#fwd must have the method dataReceived
    self.sendFlag = False
    self.transport = dummyConnection()
  def sendApplicationData(self, data) :
    self.sendFlag = True
    self._write(data)
    self.sendFlag = False
  def _write(self, data):
    #Send data if it is from applicatoin
    if self.sendFlag:
      self.fwd.dataReceived(data)
