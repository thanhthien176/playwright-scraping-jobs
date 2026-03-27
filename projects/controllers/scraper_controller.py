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
        
        # Create a worker and pass the scraping function and argument
        self._worker = ScraperWorker(industry, writer = self.writer)
        
        # Connect signal with slot
        self._worker.signals.log.connect(self.window.append_log_box)
        self._worker.signals.data_received.connect(self._on_result)
        self._worker.signals.error.connect(self._on_error)
        self._worker.signals.finished.connect(self._on_finished)
        
        self.thread_pool.start(self._worker)
        
    
    def stop_scraping(self):
        self.window.update_status('Stoped')
        if self._worker:
            self._worker.cancel()
    
    def select_db(self, table_name, filters=None):
        self.run_load_db_thread(
            self.storage.select,
            self.window.update_table_view,
            table_name,
            filters            
        )
    
    def safe_query_db(self, query_text):
        self.run_load_db_thread(
            self.storage.safe_query,
            self.window.update_table_view,
            query_text
        )
    
    def run_load_db_thread(self, fn, on_result, *args, **kwargs):
        """Load data from database into table View
        """
        # Create worker
        worker = LoadDataWorker(fn, *args, **kwargs)
        
        worker.signals.result.connect(on_result)
        worker.signals.error.connect(self._on_error)
        worker.signals.finished.connect(self._on_load_finished)
        
        self.thread_pool.start(worker)
        
    def _on_result(self, data_rows):
        self.window.append_log_box(f"Done! Scraped {len(data_rows)} jobs")
        for data in data_rows:
            self.window.add_table_row(headers=HEADER_JOB, data=data) 
        
    def _on_error(self, msg):
        self.window.append_log_box(f"Error {msg}")
        self.window.update_status("Error")
        self.window.set_button_stop()
        self.window.update_status("Error")
    
    def _on_finished(self):
        self.window.set_button_stop()
        self.window.append_log_box("Finished Scraping")
        self.window.update_status("Done")
        self.window.set_progress_finished()
        self._worker = None
    
    def _on_load_finished(self):
        self.window.update_status("Done")
            
    def get_industries(self) -> list:
        return self.storage.select("Industries")

    def append_combo_box(self):
        industries = self.get_industries()
        for industry in industries:
            self.window.add_item_box(industry)

        