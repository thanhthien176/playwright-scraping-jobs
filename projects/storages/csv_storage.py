import logging
import csv
import os
from models.job import Job

logger = logging.getLogger("storage")

class CSVStorage:
    def __init__(self, path):
        self.path = path
        self.fieldnames = ["job_id", "title", "company", "location", "min_salary", "max_salary", "url"]
        self._init_file()
    
    def _init_file(self):
        if not os.path.exists(self.path):
            try:
                with open(self.path, "w", newline="", encoding="UTF-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(self.fieldnames)
                logger.info(f"Create new CSV file: {self.path}")
                
            except Exception:
                logger.exception(f"Unable to create CSV file: {self.path}")
        
        else:
            logger.info(f"Use an existing CSV file: {self.path}")
        
    def append_job(self, job:Job):
        
        try:
            with open(self.path, "a", encoding="UTF-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    job.job_id,
                    job.title,
                    job.company,
                    job.location,
                    job.min_salary,
                    job.max_salary,
                    job.url,
                ])
        except Exception:
            logger.exception(f"Unable to add the job into CSV file: {job.url}")
                
    def load_job_id(self):
        existing_ids = set()
        
        if not os.path.exists(self.path):
            logger.info(f"CSV file does not exist: {self.path} -> returns an empty set")
            return existing_ids
        
        try:
            with open(self.path, "r", encoding="UTF-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    existing_ids.add(row["job_id"])
                
            logger.info(f"Loaded {len(existing_ids)} job IDs from CSV file")
        except Exception:
            logger.exception(f"Error when reading CSV file: {self.path}")

        return existing_ids
        
