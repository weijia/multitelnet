from twisted.internet.protocol import Protocol, ClientFactory, ServerFactory
from twisted.internet import reactor
import sys

class ForwardServer(Protocol):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.data = ""
        self._connected = False

    def dataReceived(self, data):
        #print "Received %d bytes from client\n" % len(data)
        self.data += data
        #print "%d bytes in buffer" % len(self.data)
        if self._connected and (len(self.data) > 0):
            self.connector.transport.write(self.data)
            #print "Sent %d bytes to server" % len(self.data)
            self.data = ""

    def connectionMade(self):
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

class ForwardServerFactory(ServerFactory):
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def buildProtocol(self, addr):
        return ForwardServer(self.host, self.port)

class ForwardClientFactory(ClientFactory):
    def __init__(self, forward):
        self.forward = forward

    def buildProtocol(self, addr):
        return ForwardClient(self.forward)

    def clientConnectionFailed(self, connector, reason):
        self.forward.transport.loseConnection()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "USAGE: %s <host> <port> <listen port>" % sys.argv[0]
        sys.exit(1)
    host, port, listen_port = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    server_factory = ForwardServerFactory(host, port)
    reactor.listenTCP(listen_port, server_factory)
    reactor.run()
