from models.job import Job
from storages.sqlite_storage import SQLiteStorage
import logging

logger = logging.getLogger("services")

class JobProcess:
    def __init__(self):
        self.raw_jobs = None
    
    def set_raw_jobs(self, raw_jobs: list[dict]):
        self.raw_jobs = raw_jobs
    
    def _is_valid_job(self, raw):
        if not raw:
            return False
        if not raw.get('url'):
            return False
        if not raw.get('title'):
            return False 
        return True

    def process_jobs(self, industry_id):
        if not self.raw_jobs:
            logger.warning("Raw jobs list is None, nothing to process")
            return
        
        saved = 0
        skipped = 0
        
        results = []
        
        for raw in self.raw_jobs:
            if not self._is_valid_job(raw):
                skipped += 1
                continue
            
            results.append(Job.from_raw(raw, industry_id=industry_id))
        
        return results
            
            
        
        
    