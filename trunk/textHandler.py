

class dataHandler:
  def handleData(data):
    pass


class delayHandleBase(dataHandler):
  def __init__(self, delay = 0.2):
    from twisted.internet import reactor
    self.scheduled = reactor.callLater(0, self.dummy)
    self.delay = delay
  def dummy(self):
    pass
  def delayHandle(self):
    if self.scheduled.active():
      self.scheduled.cancel()
    from twisted.internet import reactor
    self.scheduled = reactor.callLater(self.delay, self.handle)
  def handle(self):
    pass
  def handleData(self, text):#This function will be called by other class
    #print 'handle data called in delay handle base', text
    self.data.append(text)#No text removed
    self.delayHandle()
  def flushData(self):
    self.handle()
    
    
    
def complexSplit(s, splitChars):
  result = s.split(splitChars[0])
  tmpResult = []
  for i in splitChars[1:]:
    for j in result:
      tmpResult.extend(j.split(i))
    result = tmpResult
    tmpResult = []
  return result



class textHandlerLineProducer(delayHandleBase):
  def __init__(self, delay):
    self.data = []
    delayHandleBase.__init__(self, delay)

  def handle(self):
    d = ''.join(self.data)
    #print 'handle called', d
    lines = complexSplit(d, '\r\n')
    partNum = len(lines) - 1
    self.data = [lines[partNum]]
    self.linesReceived(lines)
    
  def linesReceived(self, lines):
    pass
    
  def delayCallFunc(self, func):
    #This function will add the function to callback list
    if self.callingScript:
        print 'calling script but another call request received'
        return
    self.callingScript = True
    from twisted.internet import reactor
    reactor.callLater(self.callScriptDelay, func)
  '''
  def delaySendCmd(self, cmd):
    self.cmd = cmd
    self.delayCallFunc(self.sendCmdCallback)
      
  def sendCmdCallback(self):
    self.callingScript = False
    self.notifObj(self.cmd)
  '''
