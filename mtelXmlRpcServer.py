from twisted.web import xmlrpc, server
from sessionManager import *
import uuid

'''
    dmi = mtel.sess('10.192.168.81',2001)
    mtel.uservar['mblkFound'] = False
    #Set trigger, '*ogin:$' is the trigger string it may be regular pattern
    #'root' is inputed when 'login' trigger string is met
    dmi.t = '*ogin:$','root'
    #Also set trigger, 'password:' is the trigger string, inputPass is called when 'password' trigger string is met
    dmi.t = 'password:',inputPass
    #Timeout handler, it will be called/input when timeout met
    dmi.tmo = '\n'
    #Access trigger list, disable the trigger
    dmi.trgs['*ogin:$'].en = False
    #or?
    #dmi.trgs['*ogin:$'].dis()
    #connect the session.
    dmi.con()

'''

import threading
from communication import *
'''
class notifier(threading.Thread):
  def __init__(self, data, server = 'localhost', port = 9527, authkey = "it's secret"):
    self.quitFlag = False
    self.addr = (server, port)
    self.authkey = authkey
    self.data = data
    threading.Thread.__init__(self)

  def run ( self ):
    print 'running'
    while not self.quitFlag:
      send(self.addr, self.data)
      print 'quit'
      break
  def quit(self):
    self.quitFlag = True
'''
class notifier:
  def __init__(self, data, server = 'localhost', port = 9527, authkey = "it's secret"):
    self.quitFlag = False
    self.addr = (server, port)
    self.authkey = authkey
    self.data = data
  def start(self):
    send(self.addr, self.data)
    pass
    
class callbackForRemote:
  def __init__(self, server, port):
    self.server = server
    self.port = port
  def call(self, data):
    n = notifier(data, self.server, self.port)
    n.start()


#Every xml function should return a value.
class mtelXmlRpcServer(xmlrpc.XMLRPC):
    def __init__(self):
      self.sessionMngr = sessionManager()
      self.sessionList = {}
      xmlrpc.XMLRPC.__init__(self)
    
    """An example object to be published."""
    def getSessionFromUuid(self, u):
        return self.sessionList[u]
        
    def xmlrpc_sess(self):
        """
        Create a connection
        """
        s = self.sessionMngr.createSession()
        u = str(uuid.uuid4())
        self.sessionList[u] = s
        return u
        
    def xmlrpc_con(self, sess, server, port):
        """
        Connect to server
        """
        self.sessionList[sess].connectToServer(server, port)
        return 'connecting'
    def xmlrpc_t(self, sess, pattern, command):
        """
        Set a trigger
        """
        #print 'xml t:'
        self.sessionList[sess].t = pattern, command
        return sess
    def xmlrpc_tmo(self, sess, action):
        """
        Raise a Fault indicating that the procedure should not be used.
        """
        self.sessionList[sess].tmo = action
        return sess
    def xmlrpc_c(self, sess, action):
        """
        Raise a Fault indicating that the procedure should not be used.
        """
        self.sessionList[sess].c = action
        return sess
    def xmlrpc_s(self, sess, action):
        """
        Send command to terminal
        """
        self.sessionList[sess].s = action
        return sess
    def xmlrpc_helloworld(self):
        return 'helloWorld'
    def xmlrpc_td(self, sess, action):
        self.sessionList[sess].td = action
        return sess
    def xmlrpc_tcd(self, sess, pattern):
        self.sessionList[sess].callbackTriggerOff(pattern)
        return sess
    def xmlrpc_disableAllCallback(self, sess):
        self.sessionList[sess].disableAllCallback()
        return sess
    def xmlrpc_w(self, sess, pattern, server, port):
        print 'xmlrpc_w: ',sess, pattern, server, port
        self.sessionList[sess].wait(pattern, callbackForRemote(server, port).call)
        return sess
        
    def xmlrpc_tc(self, sess, pattern, server, port):
        """
        Set a trigger
        """
        #print 'xml t:'
        print sess, pattern, server, port
        self.sessionList[sess].addCallbackTrigger(pattern, callbackForRemote(server, port).call)
        return sess
    def xmlrpc_ecp(self, sess):
        o = self.sessionList[sess].endCapture()
        #r = ''.join(o)
        #print r
        #import xmlrpclib
        #p = xmlrpclib.Binary(o)
        k = o.replace(chr(8),'')#xml rpc can not decode char 0x8
        return k
        #return sess
    def xmlrpc_scp(self, sess):
        self.sessionList[sess].startCapture()
        return sess
    def xmlrpc_disconnectRemote(self, sess):
        self.sessionList[sess].disconnectRemote()