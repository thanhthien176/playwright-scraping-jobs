import logging
from PySide6.QtCore import QObject, Signal, QRunnable
from playwright.sync_api import sync_playwright
from scraper.job_scraper import JobScraper
from services.job_service import JobProcess
from threads.write_db_thread import DataWriter
from config.logging_config import setup_logging

setup_logging()
logger = logging.getLogger("scraper_worker")
class WorkerSignal(QObject):
    log = Signal(str)
    data_received = Signal(list)
    progress = Signal(int)
    error = Signal(str)
    finished = Signal()


class ScraperWorker(QRunnable):
    def __init__(self, industry:dict, writer: DataWriter):
        super().__init__()
        self.industry = industry
        self.signals = WorkerSignal()
        self._is_cancelled = False
        self.job_process = JobProcess()
        self.writer = writer 
        
    def cancel(self):
        self._is_cancelled = True
    
    def run(self):
        browser = None
        
        with sync_playwright() as p:
            try:
            
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()    
                scraper = JobScraper(page=page)
                
                url = self.industry.get('url')
                name = self.industry.get('name')
                industry_id = self.industry.get('industry_id')
                
                scraper.goto(url=url)
                num_page = 1
                
                total = 0
                
                while True:
                    logger.info("Scraping %s - page %s", name, num_page)
                    self.signals.log.emit(f"Scraping {name} - {num_page} page")
                    
                    
                    raw_jobs = scraper.scraper_job()
                    
                    self.job_process.set_raw_jobs(raw_jobs)
                    processed_batch = self.job_process.process_jobs(industry_id).to_dict()

                    total += len(processed_batch)
                    
                    if processed_batch:
                        self.signals.data_received.emit(processed_batch)
                        self.writer.add_data("Jobs", processed_batch)
                        
                    self.signals.log.emit(f"Updated {total} jobs from {num_page} page of {name}")
                    logger.info(f"Updated {total} jobs from {num_page} page of {name}")
                    
                    if not scraper.go_to_next_page() or self._is_cancelled:
                        self.signals.log.emit("Stoped Scraping")
                        break
                    
                    num_page += 1
        
            except Exception as e:
                logger.exception("Error when start scraping")
                self.signals.error.emit(str(e))
        
            finally:
                if browser:
                    browser.close()
                self.signals.finished.emit()
    
        