from dataclasses import dataclass
import hashlib
import logging

logger = logging.getLogger("models")

@dataclass
class Job:
    job_id: str
    title: str
    company: str
    location: str
    min_salary: int
    max_salary: int
    url: str
    industry_id: str
    
    @staticmethod
    def generate_job_id(url:str) -> str:
    # Use MD5 to create a deterministic ID from URL
        return hashlib.md5(url.encode()).hexdigest()
    
    @staticmethod
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
    
    @classmethod
    def from_raw(cls, raw, industry_id):
        
        url = raw.get("url")
        job_id = cls.generate_job_id(url)
        
        min_salary, max_salary = cls.get_salary(raw.get("salary"))
        
        return cls(
            job_id=job_id,
            title=raw.get("title").strip(),
            company=raw.get("company","").strip(),
            location=raw.get("location","").strip(),
            min_salary=int(min_salary) if min_salary else None,
            max_salary=int(max_salary) if max_salary else None,
            url=raw["url"],
            industry_id=industry_id,
        )
    
   
    def to_dict(self):
        # return vars(self)
        return {
            'job_id': self.job_id, 
            'title': self.title,
            'company': self.company,
            'location': self.location,
            'min_salary': self.min_salary,
            'max_salary': self.max_salary,
            'url': self.url,
            'industry_id': self.industry_id 
        }
    
