
#from configUtil import *
import wx


class stringListManager:
    def addString(self, string):#add count if exist
        pass
    
class histItemList:
    def __init__(self, ctrl, history):
        self.ctrl = ctrl
        #Bind to certain event?
        self.history = history
    def addNew(self, string):
        pass


def restoreComboHistory(self, historyList, comboCtrl):
    i = None
    for i in historyList:
        #print i
        lastSelection = i
        comboCtrl.Insert(i, 0)
    if i == None:
        return False
    else:
        return True

def storeComboHistory(self, historyList, comboCtrl):
    pass


def fillIn(ctrl, hist):
    if ctrl.GetCount() == 0:
        return
    for i in hist:
        ctrl.Insert(i, 0)
    ctrl.SetStringSelection(hist[0])
    
def insertNew(ctrl, str):
    if ctrl.FindString(str) == wx.NOT_FOUND:
        ctrl.Insert(str, 0)
    ctrl.SetStringSelection(str)