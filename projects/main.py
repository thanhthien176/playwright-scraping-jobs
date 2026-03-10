from playwright.sync_api import sync_playwright, Page
from scraper.job_scraper import scrape_jobs
from services.job_service import process_jobs
from storages.sqlite_storage import SQLiteStorage
from db.schema import create_table_jobs
from config.logging_config import setup_logging
import logging


setup_logging()
logger = logging.getLogger("main")

def main():
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=False, slow_mo=200)
            page = browser.new_page()
            
            # url = os.getenv("LINK_SCRAPE")
          
            file_path = "data/scraper.db"
            storage = SQLiteStorage(file_path)
            create_table_jobs(storage)
            
            industries = storage.select("Industries", ["industry_id","url"])
            
            for industry in industries[2:]:
                scrape_industry(page, storage=storage, industry = industry)
            
        except Exception as e:
            logger.exception("Serious error in main()")
        
        finally:
            if browser:
                browser.close()
                logger.info("Closed the browser")
                
def scrape_industry(page:Page, storage:SQLiteStorage, industry):
    
    url = industry.get('url')
    page.goto(url)
    
    page_num = 1
    
    while True:
        logger.info("Scraping page '%s'", page_num)
        
        raw_jobs = scrape_jobs(page, url_base=page.url)
        
        process_jobs(raw_jobs,
                     storage=storage,
                     industry_id=industry['industry_id'])
        
        if not go_to_next_page(page):
            break
        
        page_num += 1


def go_to_next_page(page: Page, timeout=30000):
    btn_next = page.locator("a:has(i.svicon-chevron-right)")
    
    if btn_next.count()==0:
        return False
    
    btn_next.first.click()
    page.wait_for_load_state("load", timeout=timeout)
    
    return True


if __name__ == "__main__":
    main()