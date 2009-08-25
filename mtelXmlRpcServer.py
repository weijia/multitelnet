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