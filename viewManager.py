from termCtrl import *
from styledTextCtrlAdapterV3 import *


class viewManager:
  def __init__(self, config):
    self.views = []
    self.configuration = config
  def createView(self, session):
    child = termWin(None)
    child.adapter = styledTextAdapter(child.termWinContent, self.configuration, session)
    self.views.append(child)
    child.session = session
    child.configuration = self.configuration
    child.Show()
    return child
