import logging

class Logger:
    def __init__(self):
        self.obsevers = []
    def attach(self, observer):
        self.obsevers.append(observer)
    def detach(self, observer):
        self.obsevers.remove(observer)
    def notify(self, msg: str):
        print(msg)
        for callback in self.obsevers:
            callback(msg)

class ObservableHandler(logging.Handler):
    def __init__(self, level = 0):
        super().__init__(level)
        self.subscribers = []
    def subscribe(self, callback):
        self.subscribers.append(callback)
    def emit(self, msg):
        log_entry = self.format(msg)
        for callback in self.subscribers:
            callback(log_entry)

logger = logging.getLogger('default')
logger.setLevel(logging.INFO)

# 创建自定义 Handler
observable_handler = ObservableHandler()
observable_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s')
observable_handler.setFormatter(formatter)
logger.addHandler(observable_handler)

def debug(v):
    print(v)

def info(v):
    logger.info(v)

def success(v):
    logger.info(f':green[{v}]')

def warn(v):
    print(v)

def error(v):
    logger.info(f':red[{v}]')