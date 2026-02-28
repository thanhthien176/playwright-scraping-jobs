from playwright.sync_api import sync_playwright, Page
from scraper.job_scraper import scrape_jobs
from services.job_service import process_jobs
from storages.csv_storage import CSVStorage
from urllib.parse import urljoin
from dotenv import load_dotenv
from config.logging_config import setup_logging
import logging
import os
import traceback

load_dotenv()
setup_logging()
logger = logging.getLogger("main")

def main():
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=False, slow_mo=200)
            page = browser.new_page()
            
            # url = os.getenv("LINK_SCRAPE")
            url = os.getenv("LINK_SAMPLE")
            page.goto(url=url)
            
            file_path = "data/jobs_info.csv"
            storage = CSVStorage(file_path)
            
            existing_ids = storage.load_job_id()
            page_num = 1
                        
            # Browse all pages of the industry.
            while True:
                url_base = page.url
                logger.info(f"Currently scraping number {page_num} page")
                raw_jobs = scrape_jobs(page, url_base=url_base)
                
                process_jobs(raw_jobs, storage=storage, existing_ids=existing_ids)
                
                has_next = go_to_next_page(page=page)
                page_num += 1
                if not has_next:
                    logger.info("End of page, stop scrape")
                    break      
            
        
        except Exception as e:
            logger.exception("Serious error in main()")
        
        finally:
            if browser:
                browser.close()
                logger.info("Closed the browser")


def go_to_next_page(page: Page, timeout=30000):
    btn_next = page.locator("a:has(i.svicon-chevron-right)")
    
    if btn_next.count()==0:
        return False
    
    btn_next.first.click()
    page.wait_for_load_state("load", timeout=timeout)
    
    return True


if __name__ == "__main__":
    main()