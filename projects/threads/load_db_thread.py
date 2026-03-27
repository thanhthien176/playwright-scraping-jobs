from PySide6.QtCore import QObject, QRunnable, Signal
from storages.sqlite_storage import SQLiteStorage
from config.logging_config import setup_logging
import logging

setup_logging()
logger = logging.getLogger("load_db_thread")

class WorkerSignal(QObject):
    result = Signal(list, list) # rows, columns
    error = Signal(str)
    finished = Signal()
    
class LoadDataWorker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignal()
        
    def run(self):
        try:
            data = self.fn(*self.args, **self.kwargs)
            if data:
                columns = list(data[0].keys())
                self.signals.result.emit(data, columns)
        except Exception as e:
            self.signals.error.emit(str(e))
            logger.exception("Error retrieving from %s" ,self.table_name)
        finally:
            self.signals.finished.emit()