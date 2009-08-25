ptKey_cr = 13#Python term key enter
ptKey_newline = 10

EscCode = '\x1B['

def dumpStr(s):
  print 'dumping-----------------'
  for i in s:
    print i, ord(i)
  print 'dumping end-------------'

'''
When for this terminal's command line (python command line), it should be
'\n' as enter. But for terminal server (serial to ethernet) connection, it
should be '\r'+chr(0). What is the real value then?
'''
vt100TermDefaultKeyMapping = {
    8: chr(127),#chr(8),#Backspace
    chr(ptKey_cr): '\n',#'\r\000',#Enter, per protocol, it is the same as return#See vt100CharSender.py
    10: '\n',
    9: chr(9),#tab
    27: chr(27),#esc
    314: EscCode+'D',#wx.WXK_LEFT
    315: EscCode+'A',#wx.WXK_UP
    316: EscCode+'C',#wx.WXK_RIGHT
    317: EscCode+'B'#wx.WXK_DOWN
}


xtermDefaultKeyMapping = {
    8: chr(127),#chr(8),#Backspace
    chr(ptKey_cr): '\r\n',#'\r\000',#Enter, per protocol, it is the same as return#See vt100CharSender.py
    10: '\n',
    9: chr(9),#tab
    27: chr(27),#esc
    314: EscCode+'D',#wx.WXK_LEFT
    315: EscCode+'A',#wx.WXK_UP
    316: EscCode+'C',#wx.WXK_RIGHT
    317: EscCode+'B'#wx.WXK_DOWN
}


def nextLineAndHome(view):
  view.lineDownWithScroll(1)
  view.startOfLine()

def moveHome(view):
  view.startOfLine()

vt100TermDefaultReceivedKeyMapping = {
  '\n':nextLineAndHome,
  '\r':moveHome
}


xtermDefaultReceivedKeyMapping = {
  '\n':nextLineAndHome,
  '\r':moveHome
}

class vt100DefaultBehaviour:
  def translateSpecialChar(self, ch):
    '''
    Translate the char according to current telnet mode. And If it is not a
    special char, return None, otherwise, return the correct value
    '''
    try:
        sendCh = vt100TermDefaultKeyMapping[ch]
    except KeyError:
        #Return None if we didn't do anything for this character
        return None
    dumpStr(sendCh)
    return sendCh
    
  def translateReceivedSpecChar(self, view, ch):
    vt100TermDefaultReceivedKeyMapping[ch](view)

class xtermBehaviour:
  def translateSpecialChar(self, ch):
    '''
    Translate the char according to current telnet mode. And If it is not a
    special char, return None, otherwise, return the correct value
    '''
    try:
        sendCh = xtermDefaultKeyMapping[ch]
    except KeyError:
        #Return None if we didn't do anything for this character
        return None
    return sendCh
    
  def translateReceivedSpecChar(self, view, ch):
    xtermDefaultReceivedKeyMapping[ch](view)
