from twisted.internet.protocol import Protocol, ClientFactory, ServerFactory
from twisted.internet import reactor
import sys
from telnetClient import *


class teeTransport:
  def __init__(self, originalTransport, dupTransport):
    self.originalTransport = originalTransport
    self.dupTransport = dupTransport
  def write(self, data):
    self.originalTransport.write(data)
    self.dupTransport.write(data)


class viewTransport:
  def __init__(self, viewTrans):
    self.viewTrans = viewTrans
  def write(self, data):
    self.viewTrans.dataReceived(data)
  def loseConnection(self):
    pass

class forwardServer(Protocol):
    def __init__(self, session, fwdSrvMngr):
        self.session = session
        self.host = session['server']
        self.port = session['port']
        self.manager = fwdSrvMngr
        self.data = ""
        self.view = self.manager.createView(session)
        self._connected = False
        self.acceptedFlag = False

    def dataReceived(self, data):
        #print "Received %d bytes from client\n" % len(data)
        self.data += data
        #print "%d bytes in buffer" % len(self.data)
        if self._connected and (len(self.data) > 0):
            self.connector.transport.write(self.data)
            #print "Sent %d bytes to server" % len(self.data)
            self.data = ""

    def connectionMade(self):
        #We may only accept 1 client. More than 1 client is ignored
        if self.acceptedFlag:
          return
        self.acceptedFlag = True
        self.client = telnetForwardClient(self.view.adapter, self)
        self.transport = teeTransport(self.transport, viewTransport(self.client))
        self.connector = reactor.connectTCP(self.host, self.port, ForwardClientFactory(self))
        print "Client connected"

    def setConnected(self, flag):
        if flag:
            self.onConnected()
        else:
            self.transport.loseConnection()
        self._connected = flag

    def onConnected(self):
        if len(self.data) > 0:
            self.connector.transport.write(self.data)
            self.data = ""

    def connectionLost(self, reason):
        self.connector.transport.loseConnection()
        self._connected = False
        print "Client disonnected"



class forwardServerFactory(ServerFactory):
    def __init__(self, session, fwdSrvMngr):
        self.session = session
        self.manager = fwdSrvMngr

    def buildProtocol(self, addr):
        return forwardServer(self.session, self.manager)



class ForwardClient(Protocol):
    def __init__(self, forward):
        self.forward = forward

    def dataReceived(self, data):
        #print "Received %d bytes from server\n" % len(data)
        self.forward.transport.write(data)

    def connectionMade(self):
        print "Connected to server"
        self.forward.setConnected(True)

    def connectionLost(self, reason):
        self.forward.setConnected(False)
        print "Disconnected from server"


class ForwardClientFactory(ClientFactory):
    def __init__(self, forward):
        self.forward = forward

    def buildProtocol(self, addr):
        return ForwardClient(self.forward)

    def clientConnectionFailed(self, connector, reason):
        self.forward.transport.loseConnection()
