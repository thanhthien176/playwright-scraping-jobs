from models.job import Job
from storages.csv_storage import CSVStorage
import hashlib
import logging

logger = logging.getLogger("services")

def generate_job_id(url:str) -> str:
    # Use MD5 to create a deterministic ID from URL
    return hashlib.md5(url.encode()).hexdigest()

def get_salary(salary_str):
     # Some job posts omit currency → default to VND
    if not salary_str:
        logger.info("Salary is None -> return None")
        return None, None
    
    salary_str = salary_str.lower().strip()
    try:
        if "-" in salary_str:
            left, right = salary_str.split("-")
            
            min_salary = float(left.strip().split()[0])
            max_salary = float(right.strip().split()[0])
            
            if "triệu" in salary_str or "tr" in salary_str:
                return min_salary*1_000_000, max_salary*1_000_000
        
        else:
            value = float(salary_str.split()[0])
            if "triệu" in salary_str or "tr" in salary_str:
                value = value*1_000_000
                return value, value
        
    except (ValueError, IndexError):
        logger.warning(f"This salary string cannot parse: {salary_str} -> return None")
        return None, None
    
    return None, None

def process_jobs(raw_jobs, storage:CSVStorage, existing_ids:set):
    if not raw_jobs:
        logger.warning("raw_jobs list is None, nothing to process")
        return
    
    saved = 0
    skipped = 0
    
    for raw in raw_jobs:
        
        if not raw:
            logger.debug("Skip a job because the raw data is None")
            skipped +=1
            continue
        
        job_id = generate_job_id(raw['url'])
        
        if job_id in existing_ids:
            logger.debug(f"The job is existed, skip: {raw["url"]}")
            skipped +=1
            continue    # deduplicate
            
        min_salary, max_salary = get_salary(raw["salary"])
        
        try:
            job = Job(
                job_id=job_id,
                title=raw["title"].strip(),
                company=raw.get("company","").strip(),
                location=raw.get("location","").strip(),
                min_salary=int(min_salary) if min_salary else None,
                max_salary=int(max_salary) if max_salary else None,
                url=raw["url"]
            )
            
            storage.append_job(job)
            existing_ids.add(job_id)
            saved += 1
            logger.debug(f"Saved the job: {job.title} - {job.company}")
            
        except Exception:
            logger.exception(f"Error when create or saved the job from url: {raw.get('url')}")
            skipped += 1
    
    logger.info(f"Result: Saved - {saved} new jobs, Skipped - {skipped} jobs")
            
        
    