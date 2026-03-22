from playwright.sync_api import Page
from urllib.parse import urljoin
import logging

logger = logging.getLogger("scraper")

class JobScraper:
    def __init__(self, page:Page):
        self.page = page
        
    def goto(self, url):
        self.page.goto(url)
        
    def scraper_job(self):
        url_base = self.page.url
        
        section = self.page.locator("div.wp-container", has=self.page.locator('button:has-text("Sắp xếp")'))
        
        # get job <a> element
        a_elements = section.locator("a", has=self.page.locator("i.svicon-heart"))
        a_elements.first.wait_for()
        
        total = a_elements.count()
        logger.debug(f"Found {total} element in the page")
        list_res = []
        
        
        for i in range(total):
            
            element = a_elements.nth(i)
            
            # Get link from href of <a> element
            link = self._get_job_url(element)
            
            # Check if don't have link then skip 
            if not link:
                logger.debug(f"Link of {i} element does not exist")
                continue
            
            # Join the link with this page's url to a full link         
            url = urljoin(url_base, link)
                    
            list_res.append(self.extract_data(element, url))
        
        logger.info(f"Have scraped {len(list_res)} jobs")    
        return list_res
       
    def _get_job_url(self, element):
        if element:
            href = element.get_attribute("href")
            if href:
                if "?" in href:
                    link = href.split("?")[0]
                else:
                    link = href
                return link
        return None

    def _get_locator(self, element, locator):      
        locator = element.locator(locator)
        return locator
        
    def _safe_data(self, locator):
        try:
            return locator.inner_text(timeout=2000)
        except:
            logger.debug("Don't get text of the element")
            return None
        
    def extract_data(self, element,  url:str):
        try:
            title = self._safe_data(self._get_locator(element, "h3").first)
            company = self._safe_data(self._get_locator(element, "h3").nth(1))
            salary = self._safe_data(self._get_locator(element, "i.svicon-money-circle+ span" ))
            location = self._safe_data(self._get_locator(element, "i.svicon-location+ span"))
            
            return {
                # "id_job": id_job,
                "title": title,
                "company": company,
                "salary": salary,
                "location": location,
                "url": url,                        
            }
        except Exception:
            logger.exception(f"Error when extract data from {url}")
            return None
        
    def go_to_next_page(self, timeout=30000):
        next_locator = "a:has(i.svicon-chevron-right)"
        btn_next = self._get_locator(self.page, next_locator)
        
        if btn_next.count()==0:
            return False
        
        btn_next.first.click()
        self.page.wait_for_load_state("load", timeout=timeout)
        
        return True