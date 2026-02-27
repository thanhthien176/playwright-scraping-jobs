import csv
import os
from models.job import Job

class CSVStorage:
    def __init__(self, path):
        self.path = path
        self.fieldnames = ["job_id", "title", "company", "location", "min_salary", "max_salary", "url"]
        
        if not os.path.exists(self.path):
            with open(self.path, "w", newline="", encoding="UTF-8") as f:
                writer = csv.writer(f)
                writer.writerow(self.fieldnames)
        
    def append_job(self, job:Job):
        
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
                
    def load_job_id(self):
        exsiting_ids = set()
        
        if not os.path.exists(self.path):
            return exsiting_ids
        
        with open(self.path, "r", encoding="UTF-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                exsiting_ids.add(row["job_id"])
            
        return exsiting_ids
    
