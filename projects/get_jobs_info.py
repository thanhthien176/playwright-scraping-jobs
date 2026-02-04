from playwright.sync_api import sync_playwright, Page
from urllib.parse import urljoin
import csv
import traceback
import os
from dotenv import load_dotenv

def main():
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=False, slow_mo=200)
            page = browser.new_page()
            
            urls_list = get_url_from_file("urls_profession.csv")
            
            jobs = []
            seen = set()
            for url in urls_list[:1]:
                # Browser url
                page.goto(url[0])
                url_base = page.url
                
                # Get section has jobs info.
                section = page.locator("div.wp-container", has=page.locator('button:has-text("Sắp xếp")'))
                
                # get <a> element of job_card
                a_elements = section.locator("a", has=page.locator("i.svicon-heart"))
                
                a_elements.first.wait_for()
                  
                for element in a_elements.all():
                    link = get_job_url(element)
                    id_job = get_job_id(link)
                    
                    # Check the job is available in data
                    if check_job_available(id_job=id_job, seen=seen):
                        continue
                    
                    url = urljoin(url_base, link)
                    
                    if id_job:
                        jobs.append(extract_data(element, id_job, url))
                        seen.add(id_job)
                    
            for job in jobs[:5]:
                print(job)
                        
        except Exception as e:
            traceback.print_exc()
            
        finally:
            if browser:
                browser.close()
            
            
def get_job_url(element):
    if element:
        href = element.get_attribute("href")
        if href and "?" in href:
            link = href.split("?")[0]
            return link
    return None

def get_job_id(link):
    if link and "id" in link and "." in link:
        return link.split("id")[-1].split(".")[0]
    return None
    
def check_job_available(id_job:str, seen):
    if id_job in seen:
        print(f"This job is available: {id_job}")
        return True
    return False

def get_locator(element, field):
    try:
       
        locator = element.locator(field)
        return locator
    except Exception as e:
        print(f"Error: {e}")
        print(f"The locator {field} is not found")
        return None

def safe_data(locator):
    return locator.inner_text() if locator.count()>0 else None


def extract_data(element, id_job:str, url:str):
    try:
        locator_title = get_locator(element, "h3").first
        title = safe_data(locator_title)
        
        locator_company = get_locator(element, "h3").nth(1)
        company = safe_data(locator_company)
        
        locator_salary = get_locator(element, "i.svicon-money-circle+ span" )
        salary = safe_data(locator_salary)
        
        locator_location = get_locator(element, "i.svicon-location+ span")
        location = safe_data(locator_location)
        
        return {
            "id_job": id_job,
            "title": title,
            "company": company,
            "salary": salary,
            "location": location,
            "url": url,                        
        }
    except Exception as e:
        traceback.print_exc()


def get_url_from_file(filename):
    list_urls = []
    with open(f"data/{filename}", "r") as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            list_urls.append(row)
    
    return list_urls

def save_job_info_to_file(jobs_list, path_str="data/default.csv"):
    
    # get fieldnames of dict in jobs list
    if jobs_list and jobs_list.keys():
        fieldnames = jobs_list[0].keys()
    
    # Save jobs info in csv file
    with open(path_str, "a", newline="", encoding="UTF-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(jobs_list)
        print("Saved the jobs info data")

if __name__ =="__main__":
    main()