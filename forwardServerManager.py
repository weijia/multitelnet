from forwarder import *



class forwardServerManager:
  def __init__(self, viewManagerObj, config = None):
    self.forwardServers = {}
    #self.config = config
    self.viewMngr = viewManagerObj
    self.randomPortSeed = 234567
  def randomPort(self):
    self.randomPortSeed += 1
    return self.randomPortSeed
  def createForwardServer(self, session):
    from twisted.internet import reactor
    server_factory = forwardServerFactory(session, self)
    rndm = self.randomPort()
    reactor.listenTCP(rndm, server_factory)
    print 'listening at:',rndm
    return rndm
  def createView(self, session):
    v = self.viewMngr.createView(session)
    return v
