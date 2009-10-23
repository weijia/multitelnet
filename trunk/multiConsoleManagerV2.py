from sessionManager import *

class multiConsoleManager:
    def __init__(self, toolboxFrame, config):
        self.toolbox = toolboxFrame
        self.config = config
        self.server = startMultiConsoleCommandLineServer(self)
        self.server.startSshShellServer()


def getManholeFactory(namespace, **passwords):
    realm = manhole_ssh.TerminalRealm()

    def getManhole(_): return manhole.Manhole(namespace)
    
    realm.chainedProtocolFactory.protocolFactory = getManhole
    p = portal.Portal(realm)
    p.registerChecker(checkers.InMemoryUsernamePasswordDatabaseDontUse(**passwords))
    f = manhole_ssh.ConchFactory(p)
    return f

def getManholeTelnetFactory(namespace, **passwords):
    realm = manhole.TerminalRealm()

    def getManhole(_): return manhole.Manhole(namespace)
    
    realm.chainedProtocolFactory.protocolFactory = getManhole
    p = portal.Portal(realm)
    p.registerChecker(checkers.InMemoryUsernamePasswordDatabaseDontUse(**passwords))
    f = manhole.ConchFactory(p)
    return f


from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver

class multiConsoleCommandLine(LineReceiver):
    def connectionMade(self):
        print 'Got connection from', self.transport.client
    def connectionLost(self, reason):
        print self.transport.client, 'disconnected'
    def lineReceived(self, line):
        print line
        self.sendLine("You said: "+line)




from mtelXmlRpcServer import *
from forwarder import *
from multiTermSite import *

class startMultiConsoleCommandLineServer:
    def __init__(self, manager):
        self.manager = manager
    def startSimplestServer(self, port):
        from twisted.internet import reactor
        factory = Factory()
        factory.protocol = multiConsoleCommandLine
        reactor.listenTCP(port, factory)
        print 'starting http server'
        self.startHttpServer()
    def startHttpServer(self):
        TERM_SERVER_PORT = 8888
        from twisted.internet import reactor
        #from twisted.cred import portal, checkers
        #from twisted.conch import manhole, manhole_ssh
        '''
        links = {'Twisted': 'http://twistedmatrix.com/',
                 'Python': 'http://python.org'}
        '''
        #global gM
        site = server.Site(multiTermResourceRoot(self.manager))
        reactor.listenTCP(TERM_SERVER_PORT, site)


    def startSshShellServer(self):
        #reactor.listenTCP(2222, getManholeFactory(globals(), admin='aaa'))
        from twisted.conch import manhole_tap
        import os
        self.curPath = os.getcwd()
        svc = manhole_tap.makeService({'telnetPort':'tcp:2111',\
            'passwd':os.path.join(self.curPath,'pass.txt'),\
            'sshPort':'tcp:2222','namespace':globals()})

        svc.startService()
        print 'starting http server'
        self.startHttpServer()


