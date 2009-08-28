from twisted.web import xmlrpc, server
import mtel

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


class mtelXmpRpcServer(xmlrpc.XMLRPC):
    """An example object to be published."""
    def getSessionFromUuid(uuid):
        return mtel.getSessionFromUuid(uuid)
    def xmlrpc_sess(self, server, port):
        """
        Create a connection
        """
        return str(mtel.sess(server,port).uuid)
    def xmlrpc_con(self, sess):
        """
        Connect to server
        """
        mtel.getSessionFromUuid(sess).con()
    def xmlrpc_t(self, sess, pattern, command):
        """
        Set a trigger
        """
        getSessionFromUuid(sess).t = pattern, command
    def xmlrpc_tmo(self, action):
        """
        Raise a Fault indicating that the procedure should not be used.
        """
        getSessionFromUuid(sess).tmo = action
    def xmlrpc_c(self, action):
        """
        Raise a Fault indicating that the procedure should not be used.
        """
        getSessionFromUuid(sess).c = action
