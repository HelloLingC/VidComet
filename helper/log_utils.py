
class Logger:
    def __init__(self):
        self.obsevers = []
    def attach(self, observer):
        self.obsevers.append(observer)
    def detach(self, observer):
        self.obsevers.remove(observer)
    def notify(self, msg: str):
        for callback in self.obsevers:
            callback(msg)

logger = Logger()

def info(v):
    logger.notify(v)