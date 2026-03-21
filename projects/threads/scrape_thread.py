from PySide6.QtCore import QObject, Signal

class WorkerScrape(QObject):
    log = Signal(str)
    data = Signal(dict)
    progress = Signal(int)
    finished = Signal()
    
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.running = True
        
    def run(self):
        pass
    

class WorkerQuery(QObject):
    log = Signal(str)
    data = Signal(dict)
    progress = Signal(int)
    finished = Signal()
    
    def __init__(self, query):
        super().__init__()
        self.query = query
        self.running = True
    
    def run(self):
        pass
        