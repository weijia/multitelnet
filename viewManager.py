from telnetAppDataParser import *

class viewManager:
  def __init__(self, config):
    self.views = []
    self.configuration = config
  def createView(self, session):
    child = delayOutputParser(self.configuration, session)
    self.views.append(child)
    return child
