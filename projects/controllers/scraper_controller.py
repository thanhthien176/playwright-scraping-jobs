from PySide6.QtCore import QThreadPool
from playwright.sync_api import sync_playwright
from storages.sqlite_storage import SQLiteStorage
from scraper.job_scraper import JobScraper
from services.job_service import JobProcess
from gui.main_window import MainWindow
from threads.scrape_thread import ScraperWorker
from threads.write_db_thread import DataWriter
from threads.load_db_thread import LoadDataWorker
from config.settings import DB_PATH, HEADER_JOB
from config.logging_config import setup_logging
import logging


setup_logging()
logger = logging.getLogger("scraper_controller")


class ScrapeController:
    def __init__(self, window:MainWindow, writer: DataWriter):
        self.window = window
        self.view = self.window.scraper_tab
        self.storage = SQLiteStorage(path=DB_PATH)
        self.thread_pool =  QThreadPool()
        self.process = JobProcess()
        self.writer = writer
        self._worker = None
        self.table = self.window.table_tab
        
        
        #set
        self.thread_pool.setMaxThreadCount(5)
        self.table.set_table_headers(HEADER_JOB)
        
        
        self.append_combo_box()
    
        self.view.start_button.clicked.connect(self.start_scraping)
        self.view.stop_button.clicked.connect(self.stop_scraping)
    
    def start_scraping(self):
        industry = self.view.url_combo.currentData()
        
        if not industry:
            return
        
        self.view.start_processing()
        self.view.append_log(industry.get('name'))
        self.window.status.showMessage('Scraping...')
        
        # Create a worker and pass the scraping function and argument
        self._worker = ScraperWorker(industry, writer = self.writer)
        
        # Connect signal with slot
        self._worker.signals.log.connect(self.view.append_log)
        self._worker.signals.data_received.connect(self._on_result)
        self._worker.signals.error.connect(self._on_error)
        self._worker.signals.finished.connect(self._on_finished)
        
        self.thread_pool.start(self._worker)
        
    
    def stop_scraping(self):
        self.view.stop_processing()
        self.window.status.showMessage('Ready')
        if self._worker:
            self._worker.cancel()
    
    def load_jobs_to_ui(self, filters:dict=None):
        """Load data from database into table UI

        Args:
            filters (dict, optional): filters to retrieve data. Defaults to None.
        """
        
    def _on_result(self, data_rows):
        self.view.append_log(f"Done! Scraped {len(data_rows)} jobs")
        for data in data_rows:
            self.table.add_row(headers=HEADER_JOB, data=data) 
        
    def _on_error(self, msg):
        self.view.append_log(f"Error {msg}")
    
    def _on_finished(self):
        self.view.stop_processing()
        self._worker = None
            
    def get_industry(self):
        return self.storage.select("Industries")

    def append_combo_box(self):
        industries = self.get_industry()
        for industry in industries:
            self.view.add_item_box(industry)

        