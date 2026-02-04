from playwright.sync_api import sync_playwright, Page
from urllib.parse import urljoin
import csv
import traceback
import os
from dotenv import load_dotenv

load_dotenv()

LINK_SCRAPE = os.getenv("LINK_SCRAPE")

def main():
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=False, slow_mo = 200)
            context = browser.new_context()
            page = context.new_page()
            
            page.goto(LINK_SCRAPE)
            
            btn_list = page.locator("div").get_by_text("Tất cả các ngành")
            
            btn_list.click()
            
            label_top = page.locator("div").get_by_text("Top 10 nghề nghiệp")
            label_other = page.locator("div").get_by_text("Ngành khác")
            
            section_top = label_top.locator("+ div")
            section_other = label_other.locator("+ div")
            
            sections = []
            sections.extend(section_top.locator("a").all())
            sections.extend(section_other.locator("a").all())
            
            urls_section = []
            
            url_base = page.url
            
            for section in sections:
                url = urljoin(url_base, section.get_attribute("href"))
                urls_section.append(url)
            
            save_link(urls_section)
            print("Urls list saved in csv file")
        except Exception as e:
            traceback.print_exc()
            
        finally:
            if browser:
                browser.close()
            
     

def save_link(urls_list, name = "data/default.csv"):
    with open("data/urls_profession.csv", "w", newline="", encoding="UTF-8") as f:
        writers = csv.writer(f)
        for url in urls_list:
            writers.writerow([url])
            
            
if __name__ == "__main__":
    main()