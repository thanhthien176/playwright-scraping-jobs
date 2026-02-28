import sqlite3
import logging
import os
from models.job import Job

logger = logging.getLogger("storage")

class SQLiteStorage:
    def __init__(self, path:str):
        self.path = path
        self._init_db()
        
    def _init_db(self):
        """Create table if not exist"""
        try:
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            with self._connect() as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS Jobs(
                        job_id TEXT PRIMARY KEY,
                        title TEXT,
                        company TEXT,
                        location TEXT,
                        min_salary INTEGER,
                        max_salary INTEGER,
                        url TEXT
                    )
                """)
            logger.info(f"Connected SQLite: {self.path}")
            
        except Exception:
            logger.exception(f"Cannot initialize database: {self.path}")
            
    def _connect(self):
        # Return the connection, used with 'with' to automatically commit/rollback.
        return sqlite3.connect(self.path)
    
    def append_job(self, job:Job):
        try:
            with self._connect() as conn:
                conn.execute("""
                    INSERT OR IGNORE INTO Jobs 
                    (job_id, title, company, location, min_salary, max_salary, url)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    job.job_id,
                    job.title,
                    job.company,
                    job.location,
                    job.min_salary,
                    job.max_salary,
                    job.url,            
                ))
            logger.info(f"Appended - {job.url} - job into Jobs table")
        except Exception:
            logger.exception(f"Cannot save into the database: {job.url}")
            
    def load_job_ids(self)->set:
        try:
            with self._connect() as conn:
                rows = conn.execute("""SELECT job_id FROM Jobs""").fetchall()
            ids = {row[0] for row in rows}
            logger.info(f"Loaded {len(ids)} job IDs from the database")
            return ids
        except Exception:
            logger.exception("Error when load ids from the database")
            return set()
    
    