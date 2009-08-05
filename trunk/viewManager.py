from termCtrl import *



class viewManager:
  def __init__(self, config):
    self.views = []
    self.configuration = config
  def createView(self, session):
    child = termWin(None)
    child.initSession(self.configuration, session, self)
    child.Show()
    self.views.append(child)
    return child
