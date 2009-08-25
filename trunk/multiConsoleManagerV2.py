from termCtrl import *
from forwardServerManager import *
from viewManager import *
from clientManager import *

from sessionManager import *

class multiConsoleManager:
    def __init__(self, toolboxFrame, config):
        self.toolbox = toolboxFrame
        self.config = config
        self.server = startMultiConsoleCommandLineServer(self)
        self.server.startSshShellServer()
        self.childs = []
        self.sessionList = {}
        #self.server.startSimpleServer(1234)
        global gM
        gM = self
        self.vwMngr = viewManager(self.config)
        self.fwdSvrMngr = forwardServerManager(self.vwMngr, self.config)
        self.clientMngr = clientManager(self.vwMngr, self.config)


        
    def createTempSession(self, server, port, triggers, timeoutHandler):
        import copy
        session = copy.copy(localSession)
        import uuid
        session['sessionName'] = server+':'+str(port)+'-'+str(uuid.uuid4())+'-temp-session'
        import os
        session['server'] = server
        session['port'] = port
        session['triggers'] = triggers
        session['ansiLog'] = os.path.join(session['baseDir'], session['ansiLogName'])
        if timeoutHandler is None:
            print 'handler provided'
            session['timeoutHandler'] = timeoutHandler
        return self.openSession(session)
    #--------------------------------------------------------------------------------------------------------------------------------------------------------
    #The following functions can be called outside of this class.
    def openTmpSession(self, server, port, triggers = None, timeoutHandler = None):
        #print self.toolbox
        #print 'server:%s,port:%d'%(server,port)
        return self.createTempSession(server,port, triggers, timeoutHandler)
        
    def openFwdServer(self, session):
        return self.fwdSvrMngr.createForwardServer(session)

    def openSession(self, session):
        child = self.clientMngr.createTelnetClient(session)
        self.childs.append(child)
        return child#return the opened session
        
    def openPlayBackSession(self, session):
        child = self.clientMngr.createPlaybackClient(session)
        self.childs.append(child)
        return child#return the opened session
        
    def closeAll(self):
        for i in self.childs:
            try:
                i.Close()
            except:
                pass
    '''
    def newSession(self):
        self.toolbox.Show()
    def hello(self):
        pass
    '''


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


from twisted.web import server, resource

class LinksPage(resource.Resource):
    isLeaf = 1

    def __init__(self, links):
        resource.Resource.__init__(self)
        self.links = links

    def render(self, request):
        return "<ul>" + "".join([
            "<li><a href='%s'>%s</a></li>" % (link, title)
            for title, link in self.links.items()]) + "</ul>"


from mtelXmlRpcServer import *
from forwarder import *

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

        links = {'Twisted': 'http://twistedmatrix.com/',
                 'Python': 'http://python.org'}
        site = server.Site(LinksPage(links))
        reactor.listenTCP(TERM_SERVER_PORT, site)
        '''
        host = "zch66bld01"
        port = 22
        listen_port = 2345
        server_factory = ForwardServerFactory(host, port)
        reactor.listenTCP(listen_port, server_factory)
        '''
    def startXmlRpcServer(self):
        from twisted.internet import reactor
        r = mtelXmlRpcServer()
        reactor.listenTCP(8889, server.Site(r))
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
        self.startXmlRpcServer()







