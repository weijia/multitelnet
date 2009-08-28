#from multiprocessing.connection import Client
try:
  from multiprocessing.connection import Client
  from multiprocessing.connection import Listener

except:
  from processing.connection import Client
  from processing.connection import Listener
'''
def send(data, address):
  #from multiprocessing.connection import Listener

  address = ('localhost', 9527)     # family is deduced to be 'AF_INET'
  #listener = Listener(address, authkey = "it's secret")
  listener = Listener(address)

  conn = listener.accept()
  print 'connection accepted from', listener.last_accepted
  #data = conn.recv()
  conn.send(data)
  #conn.close()
  #listener.close()
  #print data

def receive(addr):
  #conn = Client(self.addr, self.authkey)
  conn = Client(addr)
  #conn.send(self.data)
  print 'receiving'
  data = conn.recv()
  #conn.close()
  return data

'''

from multiprocessing.managers import BaseManager
import Queue
class QueueManager(BaseManager): pass

globalQueueManager = None
import threading
queueServerInst = None

class queueServer(threading.Thread):
  def __init__(self, s):
    self.quitFlag = False
    self.s = s
    threading.Thread.__init__(self)

  def run ( self ):
    print 'running'
    self.s.serve_forever()
      
  def quit(self):
    self.quitFlag = True

def startServer(addr):
  global globalQueueManager
  class QueueManager(BaseManager): pass
  queue = Queue.Queue()
  QueueManager.register('get_queue', callable=lambda:queue)
  globalQueueManager = QueueManager(addr, authkey='abracadabra')
  s = globalQueueManager.get_server()
  global queueServerInst
  queueServerInst = queueServer(s)
  queueServerInst.start()
  return queueServerInst

def stopServer():
  global queueServerInst
  queueServerInst.quit()

def send(addr, data):
  class QueueManager(BaseManager): pass
  #QueueManager.register('get_queue', callable=lambda:queue)
  QueueManager.register('get_queue')#We should not add callable here as we are the client. Otherwise, the application will hang up.
  m = QueueManager(addr, authkey='abracadabra')
  m.connect()
  queue = m.get_queue()
  #print 'starting put---------------------------------------------------------'
  queue.put(data)
  del m
  #print 'end put---------------------------------------------------------'


def receive(addr):
  class QueueManager(BaseManager): pass
  QueueManager.register('get_queue')
  m = QueueManager(addr, authkey='abracadabra')
  m.connect()
  queue = m.get_queue()
  res = queue.get()
  import time
  return res

def startDebug():
  try:
    import multiprocessing
  except:
    import processing as multiprocessing
  import logging
  logger = multiprocessing.log_to_stderr()
  logger.setLevel(multiprocessing.SUBDEBUG)

def main():
  addr = ('localhost',9527)
  startServer(addr)
  print receive(addr)
  stopServer()
if __name__ == '__main__':
  main()