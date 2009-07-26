from telnetConnector import *

class telnetClient(appTelnetTransport):
  def sendApplicationData (self, data) :
    #Send the data directly
    self._write(data)

class dummyConnection:
    def loseConnection(self):
        pass



class telnetForwardClient (telnetClient) :
  def __init__(self, view, fwd):
    telnetClient.__init__(self, view)
    self.fwd = fwd#fwd must have the method dataReceived
    self.sendFlag = False
    self.transport = dummyConnection()
  def sendApplicationData(self, data) :
    self.sendFlag = True
    self._write(data)
    self.sendFlag = False
  def _write(self, data):
    #Send data if it is from applicatoin
    if self.sendFlag:
      self.fwd.dataReceived(data)
