
class sessTrigger:
    def __init__(self, action):
        self.en = True
        self.action = action
    def doAction(self, session):
        if self.en:
            if isinstance(self.action, str):
                return self.action
            else:
                return self.action(session)
        return None


def dummyFunc(sess):
    pass