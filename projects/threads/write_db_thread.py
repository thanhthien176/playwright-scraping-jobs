import threading
import queue
from storages.sqlite_storage import SQLiteStorage
import logging
from config.logging_config import setup_logging

setup_logging()
logger = logging.getLogger("db_thread")

class DataWriter(threading.Thread):
    def __init__(self, db_path):
        super().__init__()
        self.queue = queue.Queue()
        self.db = SQLiteStorage(db_path)
        self.daemon = True          # auto turn off when main thread turned off 
        self.running = True
        self.table_name = None
        
    def run(self):
        while self.running or not self.queue.empty():
            try:
                # Wait data in one second
                data_batch = self.queue.get(timeout=1)
                if data_batch:
                    self.db.insert_many(self.table_name, data_batch)
                self.queue.task_done()
                
            except queue.Empty:
                continue
            
            except Exception:
                logger.exception("Error inserting data in db_thread")
    
    def add_data(self, table_name:str, data_list: list[dict]):
        self.table_name = table_name
        self.queue.put(data_list)
        
    def stop(self):
        self.running = False