import logging
import logging.config
import inspect
import ConfigParser

try:
  logging.config.fileConfig("logging.conf")
  logFile = "logging.conf"
except ConfigParser.NoSectionError:
  logging.config.fileConfig("d:/tagfs/logging.conf")
  logFile = "d:/tagfs/logging.conf"


simpleLogConfigCache = {}#Used to init a logger if there is no logger setting in the config file

logSys = logging

def openLogConfig(fileName):
    try:
      config = ConfigParser.RawConfigParser()
      config.read(fileName)
    except:
      pass
    return config


def loadLogConofig(fileName):
    try:
      config = openLogConfig(fileName)
      loggerNames = getLoggerNames(config)
      for i in loggerNames:
          simpleLogConfigCache[i] = True
    except:
      pass
        
def getLoggerNames(config):
    try:
      keys = config.get('loggers', 'keys')
      loggerNames = keys.split(',')
      return loggerNames
    except:
      pass
      
def updateLogConfig(fileName, loggerName):
    try:
      config = openLogConfig(fileName)
      config.set('loggers', 'keys', config.get('loggers', 'keys')+','+loggerName)
      print 'new logger names:',config.get('loggers', 'keys')
      config.add_section('logger_'+loggerName)
      config.set('logger_'+loggerName, 'handlers', 'consoleHandler')
      config.set('logger_'+loggerName, 'propagate', '0')
      config.set('logger_'+loggerName, 'level', 'ERROR')
      config.set('logger_'+loggerName, 'qualname', loggerName)
      configfile = open(fileName, 'wb')
      config.write(configfile)
    except:
      pass
      
loadLogConofig(logFile)

def printLog(*args):
    logStr = ''
    for i in args:
        logStr += str(i)
    logger.debug(logStr)


def pL(*args):
    logStr = ''
    for i in args[1:]:
        logStr += str(i)
    args[0].debug(logStr)


def smL(*args):
    logStr = ''
    for i in args[1:]:
        logStr += str(i)
    smartProxyLogger.error(logStr)

def whosdaddy():
    try:
      return inspect.stack()[2][3]
    except:
      return 'unknown'

def changeEncoding(s):
    if type(s) == unicode:
        return s.encode('utf8')
    if type(s) == str:
        return s
    return str(s)


def cl(*args):
    p = whosdaddy()
    #print 'dady is',p
    realLogger = logging.getLogger(p)
    #print realLogger.findCaller()
    if not simpleLogConfigCache.has_key(p):
        #The logger name does not exist in the config file
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        #create formatter
        formatter = logging.Formatter("%(message)s")
        #add formatter to ch and fh
        ch.setFormatter(formatter)
        #add ch to logger
        realLogger.addHandler(ch)
        realLogger.propagate = False
        simpleLogConfigCache[p] = True
        updateLogConfig(logFile, p)
    logStr = ''
    for i in args:
        logStr += changeEncoding(i)
    #print 'calling debug'
    realLogger.error(logStr)

def ncl(*args):
    p = whosdaddy()
    #print 'dady is',p
    realLogger = logging.getLogger(p)
    #print realLogger.findCaller()
    if not simpleLogConfigCache.has_key(p):
        #The logger name does not exist in the config file
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        #create formatter
        formatter = logging.Formatter("%(message)s")
        #add formatter to ch and fh
        ch.setFormatter(formatter)
        #add ch to logger
        realLogger.addHandler(ch)
        realLogger.propagate = False
        simpleLogConfigCache[p] = True
        updateLogConfig(logFile, p)
    logStr = ''
    for i in args:
        logStr += str(i)
    #print 'calling debug'
    realLogger.debug(logStr+str(realLogger.findCaller()))

def testFunc():
    cl('hello world')
    ncl('hello world')

'''
Use case:
1. add a log simply:
cl('a','b','c')
2. remove a log simply.
ncl('a','b','c')
Requirement:
1. log system shall has a config file.
2. log system shall output the function name of the log.
3. log system shall output log when requested.
4. log system shall support turn off single log in every log output.
5. log system shall output logs when it is not turned off
6. log system shall support to record the turn off operation for a log command.
'''
if __name__ == "__main__":
    #print loadLogConofig("logging.conf")
    testFunc()
