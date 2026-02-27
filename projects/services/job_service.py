from models.job import Job
from storages.csv_storage import CSVStorage
import hashlib

def generate_job_id(url:str) -> str:
    return hashlib.md5(url.encode()).hexdigest()

def get_salary(salary_str):
    if not salary_str:
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
        
    except Exception:
        return None, None
    
    return None, None

def process_jobs(raw_jobs, file_path):
    jobs = {}
    storage = CSVStorage(file_path)
    exsiting_ids = storage.load_job_id()
    
    for raw in raw_jobs:
        job_id = generate_job_id(raw['url'])
        
        if job_id in jobs or job_id in exsiting_ids:
            continue    # deduplicate
            
        min_salary, max_salary = get_salary(raw["salary"])
        
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
        jobs[job_id] = job
        
    return list(jobs.values())