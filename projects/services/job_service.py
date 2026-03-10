from models.job import Job
from storages.sqlite_storage import SQLiteStorage
import logging

logger = logging.getLogger("services")

def is_valid_job(raw):
    if not raw:
        return False
    if not raw.get('url'):
        return False
    if not raw.get('title'):
        return False
    return True

def process_jobs(raw_jobs, storage:SQLiteStorage, industry_id):
    if not raw_jobs:
        logger.warning("raw_jobs list is None, nothing to process")
        return
    
    saved = 0
    skipped = 0
    
    for raw in raw_jobs:
        
        if not is_valid_job(raw):
            skipped +=1
            continue
                
        try:
            job = Job.from_raw(raw, industry_id)
            
            if storage.exists("Jobs", filters={"job_id": ("=", job.job_id)}):
                skipped += 1
                continue
            
            storage.append(table_name="Jobs", data= job.to_dict())
            
            saved += 1
            logger.debug(
                "Saved job '%s': '%s' - '%s'",
                job.job_id,
                job.title,
                job.company)
            
        except Exception:
            logger.exception(f"Error when create or saved the job from url: {raw.get('url')}")
            skipped += 1
    
    logger.info(f"Result: Saved - {saved} new jobs, Skipped - {skipped} jobs")
            
        
    