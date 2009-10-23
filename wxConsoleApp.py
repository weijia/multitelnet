#!/usr/bin/env python
#Boa:App:BoaApp

import wx
from twisted.internet import wxreactor
wxreactor.install()

from sessionManager import *
#import wxConsoleParentFrame
import toolboxFrame
from multiConsoleManagerV2 import multiConsoleManager

modules ={u'configUtil': [0, '', u'configUtil.py'],
 u'multiconsoleScript': [0, '', u'multiconsoleScript.py'],
 u'playBackFrame': [0, '', u'playBackFrame'],
 u'toolboxFrame': [0, '', u'toolboxFrame.py'],
 'wxConsoleParentFrame': [1,
                          'wxPython console Application',
                          u'wxConsoleParentFrame.py']}

global sessionMan
sessionMan = None
global appStartCallback


def addCallback(func):
    #print func
    global appStartCallback
    appStartCallback = func

class BoaApp(wx.App):
    def OnInit(self):
        self.main = toolboxFrame.create(None)
        self.main.Show()
        #self.consoleWin = wxConsoleParentFrame.create(self.main, self.main.configuration)
        self.main.sessionMngr = sessionManager(self.main, self.main.configuration)
        self.consoleMan = multiConsoleManager(toolboxFrame, self.main.configuration)
        global gM
        gM = self
        global sessionMan
        sessionMan = self.main.sessionMngr
        self.SetTopWindow(self.main)
        #print sessionMan
        global appStartCallback
        #print appStartCallback
        if appStartCallback != None:
            appStartCallback()
        
        return True

def startMulticonsoleProgram():
    from twisted.internet import reactor
    reactor.registerWxApp(BoaApp(0))
    reactor.run()#this will not return until main window closed



def mcpUp():
    startMulticonsoleProgram()
    
def main():
    mcpUp()


if __name__ == '__main__':
    main()
