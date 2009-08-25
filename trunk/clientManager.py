from telnetClient import telnetClient


class clientBase:
  def onViewClose(self):
    pass
  def getOptionState(self, c):
    pass
  def sendApplicationData(self, data):
    print 'clientBase sendApplicationData called'

    
class playbackClient(clientBase):
  def __init__(self, path, termWnd, view):
    self.play(path)
    self.termWnd = termWnd
    self.view = view
  def play(self, path):
    self.playbackFile = open(path,'rb')
  def step(self, num = 10):
    self.view.dataReceived(self.playbackFile.read(num))
    self.termWnd.SetFocus()
  def onViewClose(self):
    self.playbackFile.close()

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
    return view
  '''
  def createTelnetForwardClient(self, view, globalConfig, session):
    view.initSession(session)
    self.clients.append(telnetForwardClient(view,))
  '''
  def createPlaybackClient(self, session):
    view = self.vwManager.createView(session)
    #Client will be created when connection to server is made, so the following
    #code should not be put here
    #self.clients.append(telnetClient(view))
    view.setConnection(clientBase())
    view.playBack = True
    import os,wx
    import playBackFrame
    dlg = wx.FileDialog(
        view.terminalWnd, message="Choose a file", defaultDir=os.getcwd(),
        defaultFile="", wildcard="All files (*.*)|*.*",
        style=wx.OPEN | wx.CHANGE_DIR
        )
    if dlg.ShowModal() == wx.ID_OK:
        path = dlg.GetPath()
    client = playbackClient(path, view.terminalWnd, view)
    playback = playBackFrame.create(None)
    playback.view = client
    view.setConnection(playBackFrame.dummyConnection())

    playback.Show()

    view.adapter.height = 25
    view.adapter.scrollBottom = self.adapter.height-1
    return view
