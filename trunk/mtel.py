import wxConsoleApp
from trigger import *
import uuid
#used for user to communicate between sessions
uservar = {}

def execute(script):
    wxConsoleApp.addCallback(script)
    wxConsoleApp.mcpUp()

def getSessionFromUuid(aUuid):
    return wxConsoleApp.consoleMan.sessionList[aUuid]

class sess(object):
    def __init__(self, server, port = 23):
        '''
        Create a session
        '''
        #Contain triggers
        self.trgs = {}
        #global wxConsoleApp.consoleMan
        #self.man = wxConsoleApp.consoleMan
        #print wxConsoleApp.consoleMan
        #global consoleMan
        #print consoleMan
        self.server = server
        self.port = port
        self.timeoutHandler = dummyFunc
        self.triggerIndex = 0
        self.curSingleTrigger = 0
        self.singleTriggers = [[]]
        self.singleCmd = []
        self.uuid = str(uuid.uuid4())
        wxConsoleApp.consoleMan.sessionList[self.uuid] = self


    #override the assign operator
    def __setattr__(self, name, value):
        if name == 't':
            #It is setting triggers
            self.addTrigger(value[0], value[1])
        elif name == 'tmo':
            #Set timeout handler
            self.timeoutHandler = value
        elif name == 's':#Send
            self.addCmd(value)
        elif name == 'w':#wait for something
            self.addSingleTrigger(value)
        else:
            object.__setattr__(self, name, value)
    
    def addTrigger(self, pattern, action):
        '''
        if isinstance(action, str):
            #A string given, input
        '''
        self.trgs[pattern] = sessTrigger(action)
    
    def con(self):
        '''
        Start to connect to server
        
        if gMultiConsoleManager == None:
            print 'it is None'
            wxConsoleApp.addCallback(self.realConnectToServer, None)
        else:
            self.realConnectToServer()
        '''
        self.realConnectToServer()
        return True
    def realConnectToServer(self):
        wxConsoleApp.consoleMan.openTmpSess(self.server, self.port, self.trgs, self.timeoutHandler)
    def addSingleTrigger(self, value):
        self.triggerIndex += 1
        self.singleTriggers.append(value)
        self.singleCmd.append({})
        if self.triggerIndex == 1:
            self.addTrigger(value, self.singleTriggerCallback)
    def singleTriggerCallback(self, sess):
        return self.singleCmd[self.curSingleTrigger]
    def addCmd(self, value):
        self.singleCmd[self.triggerIndex].append(value)