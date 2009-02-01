

def logNameGen(logFileNameFmtString, server, port):
    from time import gmtime, strftime, localtime
    t = strftime("%Y%m%d_%H_%M_%S", localtime())
    logFileNameString = logFileNameFmtString%{"time":t,"server":server,
        "port":port}
    return logFileNameString
