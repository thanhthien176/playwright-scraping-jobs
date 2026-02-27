from playwright.sync_api import sync_playwright
from scraper import job_scraper

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
            
            raws = []
            while True:
                url_base = page.url
                raws.extend(job_scraper(url_base, page))
                
                
                btn_next = page.locator("a:has(i.svicon-chevron-right)")
                btn_next.wait_for()
                if btn_next.count()==0:
                    break
                btn_next.click()
            
            
        
        except Exception as e:
            traceback.print_exc()
        
        finally:
            if browser:
                browser.close()










if __name__ == "__main__":
    main()