from playwright.sync_api import Page
from urllib.parse import urljoin
import traceback


# Scrape all jobs in the page
def scrape_jobs(page: Page, url_base):
    
    try:
        section = page.locator("div.wp-container", has=page.locator('button:has-text("Sắp xếp")'))
        
        # get job <a> element
        a_elements = section.locator("a", has=page.locator("i.svicon-heart"))
        
        a_elements.first.wait_for()
        
        list_res = []
        for element in a_elements.all():
            
            # Get link from href of <a> element
            link = get_job_url(element)
            
            # Check if don't have link then skip 
            if not link:
                continue
            
            # Join the link with this page's url to a full link         
            url = urljoin(url_base, link)
                    
            list_res.append(extract_data(element, url))
            
        return list_res
    except Exception:
        traceback.print_exc()


# def get_job_id(link):
#     if link and "id" in link and "." in link:
#         return link.split("id")[-1].split(".")[0]
#     return None

def get_job_url(element):
    if element:
        href = element.get_attribute("href")
        if href:
            if "?" in href:
                link = href.split("?")[0]
            else:
                link = href
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
            # "id_job": id_job,
            "title": title,
            "company": company,
            "salary": salary,
            "location": location,
            "url": url,                        
        }
    except Exception as e:
        traceback.print_exc()