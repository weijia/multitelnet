import mtel#Multitelnet console manager

def inputPass(ses):#con is the session var
    if not mtel.uservar['mblkFound']:
        ses.s = 'firefox'#Send 'firefox' to the connection

def script():
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


def pyshScript():
    pysh = mtel.sess('127.0.0.1',2111)
    try:
        if mtel.uservar['pyshCreated']:
            return
    except KeyError:
        mtel.uservar['pyshCreated'] = True
    pysh.t = 'Username:$','admin'
    pysh.t = 'Password:$','wwj'
    pysh.con()
    
def main():
    mtel.execute(pyshScript)


if __name__ == '__main__':
    main()