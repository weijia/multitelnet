from telnetAppDataParser import *

class viewManager:
  def __init__(self, config):
    self.views = {}
    self.configuration = config
  def createView(self, sess):
    child = delayOutputParser(self.configuration, sess)
    self.views[child] = sess
    return child