import wxConsoleApp
from trigger import *
#from sessionManager import *


import uuid
#used for user to communicate between sessions
uservar = {}

def execute(script):
    wxConsoleApp.addCallback(script)
    wxConsoleApp.mcpUp()