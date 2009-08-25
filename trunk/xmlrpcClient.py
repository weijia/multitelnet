import xmlrpclib
#Port 80 is the default
'''
server = xmlrpclib.ServerProxy("http://localhost:8889")
currentTimeObj = server.helloworld()
print currentTimeObj
'''
server = xmlrpclib.ServerProxy("http://localhost:8889")
sessid = server.sess()
print sessid
import time

server.t(sessid, '\'gM\'','dir(gM)\r')

server.con(sessid, 'localhost', 2111)

time.sleep(3)
server.s(sessid, 'admin\r')

time.sleep(3)
server.s(sessid, 'wwj\r')

time.sleep(3)
server.s(sessid, 'dir()\r')

server.td(sessid, '\'gM\'')#Disable the trigger