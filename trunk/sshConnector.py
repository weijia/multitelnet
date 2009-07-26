from __future__ import nested_scopes
import os
from vt100DefaultBehaviour import *

#import Tkinter, tkFileDialog, tkFont, tkMessageBox, string
#from twisted.conch.ui import tkvt100
from twisted.conch.ssh import transport, userauth, connection, common, keys
from twisted.conch.ssh import session, forwarding, channel
#from twisted.conch.client.default import isInKnownHosts
from twisted.internet import reactor, defer, protocol, tksupport
#from twisted.python import usage, log
import getpass
from telnetConnector import *
import struct


sshTermKeyMapping = {
    8: chr(127),#chr(8),#Backspace
    13: '\r',#Enter, per protocol, it is the same as return
    9: chr(9),#tab
    27: chr(27),#esc
    314: EscCode+'D',#wx.WXK_LEFT
    315: EscCode+'A',#wx.WXK_UP
    316: EscCode+'C',#wx.WXK_RIGHT
    317: EscCode+'B'#wx.WXK_DOWN
}


class appSshTransport():
    def __init__(self, view):
        self.view = view
        view.connection = self
        #self.protocol = self.protocol = optionLogTelnetProtocol(self)
        #Telnet.__init__(self)
        #self.negotiationMap[chr(24)] = self.sendTermType
        #self.negotiationMap[chr(0x1f)] = self.sendWindowSize
    '''
    def connectionMade(self):
        #Called after connected
        
        #Call original function
        TelnetTransport.connectionMade(self)
    '''
    def loseConnection(self):
        pass
    def dataReceived(self, data):
        self.applicationDataReceived(data)
        
    def applicationDataReceived(self, data):
        self.view.write(data)
        #print data
    def _write(self, data):
        self.transport.write(data)
    def writeCtrlKey(self, key):#Key should only be 'A'-'Z'
        #"CTRL" key pressed with key.
        sendKey = key-ord('A')+1#'A' will send 1 to server
        '''
        if self.getOptionState(chr(01)).him.state == 'no':
            #Server will not echo, so we need to echo, it should be ^A etc.
            self.view.log('will echo')
            if key>255:
                self.view.log('out of 256%d'%key)
            else:
                self.view.write('^'+chr(key))
        '''
        self._write(chr(sendKey))
        return False#tell the window msg hendler do not process the message again

    def writeKey(self, key):
        #Translate the input key according to current telnet mode.
        print 'sending key'
        try:
            sendKey = sshTermKeyMapping[key]
        except KeyError:
            try:
                print 'no mapping'
                self.view.log('no mapping: %d'%key)
            except:
                print 'key is not int:%c'%key
                self.view.log('no mapping: %d'%ord(key))
            return True
        self.write(sendKey)
        print 'entered:%c,%d'%(chr(key),key)
        return False
        
    def write(self, data):
        '''
        s = self.getOptionState(chr(01))#ECHO?
        if s.him.state == 'no':
            #Server will not echo, so we need to echo
            #logging.error('our echo state:'+str(s.us.state))
            #print 'server echo state:'+s.him.state
            self.view.write(data)
        #print 'our echo state:'+s.us.state
        '''
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
        '''
        self.requestNegotiation('termtype', chr(24)+chr(0)+'vt100')
        '''
        #self.sendWindowSize()
        
    def sendWindowSize(self):
        #self.will(chr(24))#need not since it is acked already
        #The server seems do not reply for the above command, send it manually
        #Write termtype to server
        '''
        self.requestNegotiation('windSize', chr(0x1f)+\
            chr((self.view.getWidth()&0xff00)>>8)+chr((self.view.getWidth()&0xff))+\
            chr((self.view.getHeight()&0xff00)>>8)+chr((self.view.getHeight()&0xff))
            )
        print 'winsize width:%d'%self.view.getWidth()
        print 'winsize height:%d'%self.view.getHeight()
        '''

        
    def callbackfunc(self, option):
        logging.error('callback called')
        self.will(option)


class SSHClientFactory(protocol.ClientFactory):
    def __init__(self, view):
        self.view = view
        
    def buildProtocol(self, addr):
        return SSHClientTransport(self.view)

    def clientConnectionFailed(self, connector, reason):
        print ('TkConch','Connection Failed, Reason:\n %s: %s' % (reason.type, reason.value))

class SSHClientTransport(transport.SSHClientTransport):
    def __init__(self, view):
        self.view = view

    def receiveError(self, code, desc):
        global exitStatus
        exitStatus = 'conch:\tRemote side disconnected with error code %i\nconch:\treason: %s' % (code, desc)

    def sendDisconnect(self, code, reason):
        global exitStatus
        exitStatus = 'conch:\tSending disconnect with error code %i\nconch:\treason: %s' % (code, reason)
        transport.SSHClientTransport.sendDisconnect(self, code, reason)

    def receiveDebug(self, alwaysDisplay, message, lang):
        global options
        #if alwaysDisplay or options['log']:
        #    log.msg('Received Debug Message: %s' % message)
        print('Received Debug Message: %s' % message)

    def verifyHostKey(self, hostKey, fingerprint):
        print 'host key fingerprint: %s' % fingerprint
        return defer.succeed(1)


    def connectionSecure(self):
        user = getpass.getuser()
        self.requestService(SSHUserAuthClient(user, SSHConnection(self.view), self.view))

class SSHUserAuthClient(userauth.SSHUserAuthClient):
    def __init__(self, user, conn, view):
        self.view = view
        userauth.SSHUserAuthClient.__init__(self, user, conn)
        self.kept = ''

    def getPassword(self):
        self.view.write('Password:')
        self.view.connection = self
        return self.view.getPassword()
    
    def getPublicKey(self):
        return  # Empty implementation: always use password auth
    
    def sendWindowSize(self):
        pass
    
    def write(self, data):
        self.writeChar(data)
    
    def writeChar(self, data):
        #print 'auth start write data:%s'%data
        self.kept += data
        keptParts = self.kept.split('\r')
        #print keptParts
        #print data
        #print ord(data[-1])
        #print '----------------'
        if (len(keptParts) > 1) or (data[-1] == '\r'):
            self.kept = '\r'.join(keptParts[1:])
            self.sendString(keptParts[0])
        print 'writing data'
        
    def writeKey(self, keyCode):
        '''
        This function should return False, if the key should not 
        '''
        if keyCode == 13:
            self.sendString(self.kept)
            self.kept = ''
            return False
        if keyCode == 8:
            self.kept = self.kept[0:-1]
            return False
        return True
    
    def sendString(self, text):
        self.view.write('\r\n')
        self.view.getPassDefer.callback(self.kept)
        #print 'entering data:%s'%self.kept
        
    def loseConnection(self):
        pass

class SSHConnection(connection.SSHConnection):
    def __init__(self, view):
        self.view = view
        connection.SSHConnection.__init__(self)

    def serviceStarted(self):
        self.openChannel(SSHSession(self.view))

class SSHSession(channel.SSHChannel):
    name = 'session'
    def __init__(self, view):
        self.view = view
        self.appTelnet = appSshTransport(self.view)
        channel.SSHChannel.__init__(self)
        
    def channelOpen(self, foo):
        c = session.SSHSessionClient()
        c.dataReceived = self.write
        #self.appTelnet.conn = self.conn
        c.connectionLost = self.sendEOF
        self.appTelnet.transport = self
        term = os.environ.get('TERM', 'xterm')
        #winsz = fcntl.ioctl(fd, tty.TIOCGWINSZ, '12345678')
        winSize = (25,80,0,0) #struct.unpack('4H', winsz)
        ptyReqData = session.packRequest_pty_req(term, winSize, '')
        self.conn.sendRequest(self, 'pty-req', ptyReqData)
        self.conn.sendRequest(self, 'shell', '')
        self.conn.transport.transport.setTcpNoDelay(1)
        

    def dataReceived(self, data):
        self.appTelnet.dataReceived(data)

    def extReceived(self, t, data):
        if t==connection.EXTENDED_DATA_STDERR:
            log.msg('got %s stderr data' % len(data))
            sys.stderr.write(data)
            sys.stderr.flush()

    def eofReceived(self):
        print('got eof')
        sys.stdin.close()

    def closed(self):
        print('closed %s' % self)


    def request_exit_status(self, data):
        global exitStatus
        exitStatus = int(struct.unpack('>L', data)[0])
        print('exit status: %s' % exitStatus)

    def sendEOF(self):
        self.conn.sendEOF(self)
        
def connectSsh(session, view):
    from twisted.internet import reactor
    try:
        port = session['port']
    except KeyError:
        port = 22
    try:
        if not view.playBack:
            reactor.connectTCP(session['server'],port,SSHClientFactory(view))
        else:
            fact = telnetFactory(view)
    except:
        reactor.connectTCP(session['server'],port,SSHClientFactory(view))
        
class consoleView:
    def write(self, data):
        print data


def main():
    sessionInfo = {'server':'zch66bld01'}
    print 'step1'
    view = consoleView()
    print 'step2'
    connectSsh(sessionInfo,view)
    print 'step3'
    reactor.run()
    
if __name__ == '__main__':
    main()
