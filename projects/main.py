from playwright.sync_api import sync_playwright, Page
from scraper.job_scraper import scrape_jobs
from services.job_service import process_jobs

from urllib.parse import urljoin
from dotenv import load_dotenv
import os
import traceback

load_dotenv()
def main():
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=False, slow_mo=200)
            page = browser.new_page()
            
            url = os.getenv("LINK_SCRAPE")
            page.goto(url=url)
            
            result = []
                        
            # Browse all pages of the industry.
            while True:
                url_base = page.url
                raw_jobs = scrape_jobs(url_base, page)
                
                result.extend(process_jobs(raw_jobs=raw_jobs))
                
                go_to_next_page(page=page)
            
                
            
                
            
            
        
        except Exception as e:
            traceback.print_exc()
        
        finally:
            if browser:
                browser.close()


def go_to_next_page(page: Page, timeout=3000):
    btn_next = page.locator("a:has(i.svicon-chevron-right)")
    
    if btn_next.count()==0:
        return False
    
    btn_next.first.click()
    page.wait_for_load_state("networkidle", timeout=timeout)
    return True








if __name__ == "__main__":
    main()