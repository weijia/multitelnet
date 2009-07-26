

class clientManager:
  def __init__(self):
    self.clients = []
  def createTelnetClient(self, view, globalConfig, session):
    view.initSession(session)
    self.clients.append(telnetClient(view))
  '''
  def createTelnetForwardClient(self, view, globalConfig, session):
    view.initSession(session)
    self.clients.append(telnetForwardClient(view,))
  '''
