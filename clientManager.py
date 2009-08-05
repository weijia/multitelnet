from telnetClient import telnetClient






class clientBase:
  def onViewClose(self):
    pass
  def getOptionState(self, c):
    pass
  def sendApplicationData(self, data):
    pass


class clientManager:
  def __init__(self, vwManager, config):
    self.clients = []
    self.vwManager = vwManager
    self.config = config
  def createTelnetClient(self, session):
    from telnetConnector import connectTelnet
    from sshConnector import connectSsh
    view = self.vwManager.createView(session)
    #Client will be created when connection to server is made, so the following
    #code should not be put here
    #self.clients.append(telnetClient(view))
    view.setConnection(clientBase())
    if session['sshFlag']:
        connectSsh(session, view)
    else:
        connectTelnet(session, view)
  '''
  def createTelnetForwardClient(self, view, globalConfig, session):
    view.initSession(session)
    self.clients.append(telnetForwardClient(view,))
  '''
