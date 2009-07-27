from telnetClient import *

class telnetFactory(ClientFactory):
    def __init__(self, view):
        self.view = view
    def startedConnecting(self,connector):
        print("Start to connect")
    def buildProtocol(self,addr):
        print("build protocol")
        return telnetClient(self.view)
    def clientConnectionLost(self,connector,reason):
        self.view.clientConnectionLost(reason)
        print("client connection lost" + str(reason))
    def clientConnectionFailed(self,connector,reason):
        self.view.clientConnectionFailed(reason)
        print("client connection failed" + str(reason))

def connectTelnet(session, view):
    from twisted.internet import reactor
    try:
        port = session['port']
    except KeyError:
        port = 23
    try:
        if not view.playBack:
            reactor.connectTCP(session['server'],port,telnetFactory(view))
        else:
            fact = telnetFactory(view)
    except:
        reactor.connectTCP(session['server'],port,telnetFactory(view))
        
class consoleView:
    def write(self, data):
        print data


def main():
    sessionInfo = {'server':'bbs.nju.edu.cn'}
    print 'step1'
    view = consoleView()
    print 'step2'
    connectTelnet(sessionInfo,view)
    print 'step3'
    reactor.run()
    
    

if __name__ == '__main__':
    main()
