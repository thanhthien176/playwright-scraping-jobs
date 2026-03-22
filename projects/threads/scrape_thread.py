from PySide6.QtCore import QObject, Signal, QRunnable

class WorkerSignal(QObject):
    log = Signal(str)
    result = Signal(object)
    progress = Signal(int)
    error = Signal(str)
    finished = Signal()


class ScraperWorker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignal()
        self._is_cancelled = False
        
    def cancel(self):
        self._is_cancelled = True
    
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
            self.signals.result.emit(result)
        except Exception as e:
            self.signals.error.emit(str(e))
        
        finally:
            self.signals.finished.emit()
        
        