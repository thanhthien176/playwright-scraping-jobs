from PySide6.QtCore import QObject, QRunnable, Signal
from storages.sqlite_storage import SQLiteStorage
from config.logging_config import setup_logging
import logging

setup_logging()
logger = logging.getLogger("load_db_thread")

class WorkerSignal(QObject):
    result = Signal(list)
    columns = Signal(list)
    error = Signal(str)
    finished = Signal()
    
class LoadDataWorker(QRunnable):
    def __init__(self, storage: SQLiteStorage, table_name, filters=None):
        super().__init__()
        self.storage = storage
        self.table_name = table_name
        self.filters = filters
        self.signals = WorkerSignal()
        
    def run(self):
        try:
            data = self.storage.select(self.table_name, filters=self.filters)
            schema = self.storage.schema(self.table_name).keys()
            
            # self.signals.columns.emit(schema if schema else [])
            self.signals.result.emit(data if data else [])
        except Exception as e:
            self.signals.error.emit(str(e))
            logger.exception("Error retrieving from %s" ,self.table_name)