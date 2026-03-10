from storages.sqlite_storage import SQLiteStorage


def create_table_jobs(storage:SQLiteStorage):
    storage.create_table("Jobs", {
        "job_id": "TEXT PRIMARY KEY",
        "title": "TEXT",
        "company": "TEXT",
        "location": "TEXT",
        "min_salary": "INTEGER",
        "max_salary": "INTEGER",
        "url": "TEXT",
        "industry_id": "TEXT",
    })