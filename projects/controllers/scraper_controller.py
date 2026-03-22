from PySide6.QtCore import QThreadPool
from playwright.sync_api import sync_playwright

from storages.sqlite_storage import SQLiteStorage
from scraper.job_scraper import JobScraper
from services.job_service import JobProcess
from gui.main_window import MainWindow
from threads.scrape_thread import ScraperWorker
from config.settings import DB_PATH
from config.logging_config import setup_logging
import logging


setup_logging()
logger = logging.getLogger("scraper_controller")


class ScrapeController:
    def __init__(self, window:MainWindow):
        self.window = window
        self.view = self.window.scraper_tab
        self.storage = SQLiteStorage(path=DB_PATH)
        self.thread_pool =  QThreadPool()
        self.process = JobProcess()
        self._worker = None
        
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
        self._worker = ScraperWorker(self.scraping, industry)
        
        # Connect signal with slot
        self._worker.signals.log.connect(self.view.append_log)
        self._worker.signals.result.connect(self._on_result)
        self._worker.signals.error.connect(self._on_error)
        self._worker.signals.finished.connect(self._on_finished)
        
        self.thread_pool.start(self._worker)
        
    
    def stop_scraping(self):
        self.view.stop_processing()
        self.window.status.showMessage('Ready')
        if self._worker:
            self._worker.cancel()
        
    
    def scraping(self, industry: dict):
        with sync_playwright() as p:
            Jobs = []
            
            try:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()    
                self.scraper = JobScraper(page=page)
                
                self.scraper.goto(industry.get('url'))
                
                num_page = 1
                
                while True:
                    logger.info("Scraping %s - page %s", industry.get('name'), num_page)
                    
                    raw_jobs = self.scraper.scraper_job()
                    
                    self.process.set_raw_jobs(raw_jobs)
                    Jobs.extend(self.process.process_jobs(industry.get('id')))
                    
                    self._worker.signals.log.emit(f"Scraping {industry.get('name')} - {num_page} page")
                    
                    if self._worker and self._worker._is_cancelled:
                        self._worker.signals.log.emit("Stoped Scraping")
                        break
                    
                    if not self.scraper.go_to_next_page():
                        break
                    
                    num_page += 1
           
            except Exception as e:
                logger.exception("Error when start scraping")
                self._worker.signals.error.emit(str(e))
            
            finally:
                if browser:
                    browser.close()
            return Jobs
    
    def _on_result(self, jobs):
        self.view.append_log(f"Done! Scraped {len(jobs)} jobs")
        
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
        
    
    # def browse_industry(self):
    
    #     url = industry.get('url')
        
    #     self.scraper.goto(url)
        
    #     page_num = 1
        
    #     while True:
    #         logger.info("Scraping page '%s'", page_num)
            
    #         raw_jobs = self.scraper.scraper_job()
            
    #         self.process.process_jobs(raw_jobs, industry_id=industry.get('industry_id'))
            
    #         if not self.scraper.go_to_next_page():
    #             break
            
    #         page_num += 1

    