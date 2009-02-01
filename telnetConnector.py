
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

import logging
'''
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='d:\\log.txt',
                    filemode='w')
'''
EscCode = '\x1B['

vt100TermKeyMapping = {
    8: chr(127),#chr(8),#Backspace
    13: '\r\n',#Enter, per protocol, it is the same as return
    9: chr(9),#tab
    27: chr(27),#esc
    314: EscCode+'D',#wx.WXK_LEFT
    315: EscCode+'A',#wx.WXK_UP
    316: EscCode+'C',#wx.WXK_RIGHT
    317: EscCode+'B'#wx.WXK_DOWN
}

#Not fully understood
vt100TermKeyComplexMapping = {
    #input  telnetOption    enabledValue    disabledValue
    13:     [0x22,          ['\r\n',        '\r'+chr(0)]]#Enter
}


class optionLogTelnetProtocol(TelnetProtocol):
    def __init__(self, protocol):
        self.protocol = protocol
        self.negFlag = False
        
    def unhandledCommand(self, command, argument):
        try:
            logging.error('unhandledCmd:'+command + argument)
        except:
            logging.error('unhandledCmd')

    def unhandledSubnegotiation(self, command, bytes):
        logging.error('unhandledNeg:'+command + bytes)

    def enableLocal(self, option):
        if None != self.negFlag :
            self.negFlag = True
        if option == chr(24):
            logging.error('enableLocal termtype 24')
            return True
            #self.protocol.sendTermType()
        elif option == chr(01):#ECHO
            logging.error('enableLocal echo')
            return True
        elif option == NAWS:
            #self.protocol.will(option)
            return True
        logging.error('enableLocal:'+ option)
        #self.sendInitialNeg()#We send initial neg only we received neg command so we are sure the other part support telnet protocol

    def enableRemote(self, option):
        #The remote here is said from the server side, so it's server ask client to support echo?
        #Answser is no. Server is offer to let himself enable ECHO
        if option == chr(01):#ECHO
            logging.error('enableRemote echo')
            #We are echoing so ask server do no echo
            return True
        logging.error('enableRemote:'+ option)

    def disableLocal(self, option):
        logging.error('disableLocal:'+ option)

    def disableRemote(self, option):
        logging.error('disableRemote:'+ option)
    '''
    def sendInitialNeg(self):
        if self.negFlag:
            self.protocol.sendTermType()
            self.negFlag = None
    '''

class appTelnetTransport(TelnetTransport):
    def __init__(self, view):
        self.view = view
        view.connection = self
        self.protocol = self.protocol = optionLogTelnetProtocol(self)
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
        self.view.write(data)
        #print data
    def writeCtrlKey(self, key):#Key should only be 'A'-'Z'
        #"CTRL" key pressed with key.
        sendKey = key-ord('A')+1#'A' will send 1 to server
        if self.getOptionState(chr(01)).him.state == 'no':
            #Server will not echo, so we need to echo, it should be ^A etc.
            self.view.log('will echo')
            if key>255:
                self.view.log('out of 256%d'%key)
            else:
                self.view.write('^'+chr(key))
        self._write(chr(sendKey))
        return False#tell the window msg hendler do not process the message again

    def writeKey(self, key):
        #Translate the input key according to current telnet mode.
        try:
            sendKey = vt100TermKeyMapping[key]
        except KeyError:
            self.view.log('no mapping: %d'%key)
            return True
        self.write(sendKey)
        #print 'entered:%c,%d'%(chr(key),key)
        return False
        
    def write(self, data):
        s = self.getOptionState(chr(01))#ECHO?
        if s.him.state == 'no':
            #Server will not echo, so we need to echo
            #logging.error('our echo state:'+str(s.us.state))
            #print 'server echo state:'+s.him.state
            self.view.write(data)
        #print 'our echo state:'+s.us.state
        self._write(data)
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
            logging.error('neo 24')
        elif option == chr(01):
            logging.error('echo')
            #self.protocol.will(option)
        elif option == NAWS:
            #self.protocol.will(option)
            value = self._OptionState()
            value.us = self._Perspective()
            value.him = self._Perspective()
            return self.options.setdefault(opt, )
        
        logging.error('enableLocal:'+ option)
        return TelnetTransport.getOptionState(self, option)
    '''
    
    def sendTermType(self, bytes):
        #self.will(chr(24))#need not since it is acked already
        #The server seems do not reply for the above command, send it manually
        #Write termtype to server
        self.requestNegotiation('termtype', chr(24)+chr(0)+'vt100')
        #self.sendWindowSize()
        
    def sendWindowSize(self):
        #self.will(chr(24))#need not since it is acked already
        #The server seems do not reply for the above command, send it manually
        #Write termtype to server
        self.requestNegotiation('windSize', chr(0x1f)+\
            chr((self.view.getWidth()&0xff00)>>8)+chr((self.view.getWidth()&0xff))+\
            chr((self.view.getHeight()&0xff00)>>8)+chr((self.view.getHeight()&0xff))
            )

        
    def callbackfunc(self, option):
        logging.error('callback called')
        self.will(option)
        
class telnetFactory(ClientFactory):
    def __init__(self, view):
        self.view = view
    def startedConnecting(self,connector):
        print("Start to connect")
    def buildProtocol(self,addr):
        print("build protocol")
        return appTelnetTransport(self.view)
    def clientConnectionLost(self,connector,reason):
        self.view.clientConnectionLost(reason)
        print("client connection lost" + str(reason))
    def clientConnectionFailed(self,connector,reason):
        self.view.clientConnectionFailed(reason)
        print("client connection failed" + str(reason))

def connectTelnet(session, view):
    from twisted.internet import reactor
    try:
        port = session['port']
    except KeyError:
        port = 23
    try:
        if not view.playBack:
            reactor.connectTCP(session['server'],port,telnetFactory(view))
        else:
            fact = telnetFactory(view)
    except:
        reactor.connectTCP(session['server'],port,telnetFactory(view))
        
class consoleView:
    def write(self, data):
        print data


def main():
    sessionInfo = {'server':'bbs.nju.edu.cn'}
    print 'step1'
    view = consoleView()
    print 'step2'
    connectTelnet(sessionInfo,view)
    print 'step3'
    reactor.run()
    
    

if __name__ == '__main__':
    main()
