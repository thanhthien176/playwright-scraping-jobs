from dataclasses import dataclass

@dataclass
class Job:
    job_id: str
    title: str
    company: str
    location: str
    min_salary: int
    max_salary: int
    url: str