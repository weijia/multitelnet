

from twisted.web import server, resource


def changeToAscii(code):
  n = ""
  for i in code:
    try:
      n += str(i)
    except:
      n += "?"
  return n

class multiTermResourceBase(resource.Resource):
  def __init__(self, consoleMan):
    resource.Resource.__init__(self)
    self.consoleMan = consoleMan  

    
class multiTermResourceRoot(multiTermResourceBase):
  def getChild(self, name, request):
    if name == '':
      return multiTermSite(self.consoleMan)
    return sampleLeaf()

class sampleLeaf(resource.Resource):
  isLeaf = 1
  def render(self, request):
    print 'hello world'
    return """<html>
      Hello, world! I am located at %r.
    </html>"""% (request.prepath)
    
class multiTermSite(resource.Resource):
  isLeaf = 1

  def __init__(self, consoleMan):
    resource.Resource.__init__(self)
    self.consoleMan = consoleMan
  def genDict(self, d):
    if type(d) is dict:
      s = "<ul>"
      for i in d.keys():
        try:
          s += "<li>"+str(i)+":<br/>"
        except:
          s += "<li>"+changeToAscii(i)+"<br/>"
        s += self.genDict(d[i])
        s += "</li>"
      s += "</ul>"
      return s
    elif type(d) is list:
      s = "<ul>"
      for i in d:
        try:
          s += "<li>"+str(i)+":<br/>"
        except:
          s += "<li>"+changeToAscii(i)+"<br/>"
        s += "</li>"
      s += "</ul>"
      return s
    else:
      return str(d)
  def render(self, request):
    return str(self.genDict(self.consoleMan.config))