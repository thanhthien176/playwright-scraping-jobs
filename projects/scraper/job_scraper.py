from playwright.sync_api import Page
from urllib.parse import urljoin
import traceback


def scrape_jobs(url_base, page: Page):
    
    section = page.locator("div.wp-container", has=page.locator('button:has-text("Sắp xếp")'))
        
    # get job <a> card
    a_elements = section.locator("a", has=page.locator("i.svicon-heart"))
    
    a_elements.first.wait_for()
    
    list_res = []
    for element in a_elements.all():
        link = get_job_url(element)
        # id_job = get_job_id(link)
        if not link:
            continue
        
        url = urljoin(url_base, link)
                
        list_res.append(extract_data(element, url))
    
    return list_res
        

def get_job_url(element):
    if element:
        href = element.get_attribute("href")
        if href and "?" in href:
            link = href.split("?")[0]
            return link
    return None

def get_locator(element, locator):      
    locator = element.locator(locator)
    return locator
        
def safe_data(locator):
    try:
        return locator.inner_text(timeout=2000)
    except:
        traceback.print_exc()
        return None
        
def extract_data(element,  url:str):
    try:
        title = safe_data(get_locator(element, "h3").first)
        company = safe_data(get_locator(element, "h3").nth(1))
        salary = safe_data(get_locator(element, "i.svicon-money-circle+ span" ))
        location = safe_data(get_locator(element, "i.svicon-location+ span"))
        
        return {
            "title": title,
            "company": company,
            "salary": salary,
            "location": location,
            "url": url,                        
        }
    except Exception as e:
        traceback.print_exc()