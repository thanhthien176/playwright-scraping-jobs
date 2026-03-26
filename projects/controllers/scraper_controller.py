from PySide6.QtCore import QThreadPool
from playwright.sync_api import sync_playwright
from services.job_service import JobProcess
from storages.sqlite_storage import SQLiteStorage
from threads.scrape_thread import ScraperWorker
from threads.write_db_thread import DataWriter
from threads.load_db_thread import LoadDataWorker
from config.settings import DB_PATH, HEADER_JOB
from config.logging_config import setup_logging
import logging


setup_logging()
logger = logging.getLogger("scraper_controller")


class ScrapeController:
    def __init__(self, window, writer: DataWriter):
        self.window = window
        self.storage = writer.db if writer else SQLiteStorage(DB_PATH)
        self.thread_pool =  QThreadPool()
        self.process = JobProcess()
        self.writer = writer
        self._worker = None
        
        
        #set
        self.thread_pool.setMaxThreadCount(5)
        self.window.set_table_tab_headers(HEADER_JOB)
        
        
        self.append_combo_box()
    
    def start_scraping(self):
        industry = self.window.get_industry()
        
        if not industry:
            return
        
        self.window.append_log_box(industry.get('name'))
        self.window.update_status('Scraping...')
        
        # Create a worker and pass the scraping function and argument
        self._worker = ScraperWorker(industry, writer = self.writer)
        
        # Connect signal with slot
        self._worker.signals.log.connect(self.window.append_log_box)
        self._worker.signals.data_received.connect(self._on_result)
        self._worker.signals.error.connect(self._on_error)
        self._worker.signals.finished.connect(self._on_finished)
        
        self.thread_pool.start(self._worker)
        
    
    def stop_scraping(self):
        self.window.update_status('Ready')
        if self._worker:
            self._worker.cancel()
    
    def load_data_to_ui(self, table_name, filters:dict=None):
        """Load data from database into table UI

        Args:
            filters (dict, optional): filters to retrieve data. Defaults to None.
        """
        # Create worker
        worker = LoadDataWorker(self.storage, table_name=table_name, filters=filters)
        
        worker.signals.result.connect(self.window.update_table_view)
        # worker.signals.columns.connect(self.window.update_columns)
        worker.signals.error.connect(self._on_error)
        
        self.thread_pool.start(worker)
        
    def _on_result(self, data_rows):
        self.window.append_log_box(f"Done! Scraped {len(data_rows)} jobs")
        for data in data_rows:
            self.window.add_table_row(headers=HEADER_JOB, data=data) 
        
    def _on_error(self, msg):
        self.window.append_log_box(f"Error {msg}")
    
    def _on_finished(self):
        self.window.set_button_stop()
        self.window.append_log_box("Finished Scraping")
        self._worker = None
            
    def get_industries(self) -> list:
        return self.storage.select("Industries")

    def append_combo_box(self):
        industries = self.get_industries()
        for industry in industries:
            self.window.add_item_box(industry)

        