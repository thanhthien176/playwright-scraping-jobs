# Job Scraping Tool

## Overview
This project is a job scraping tool built with Python and Playwright.
The goal is to collect job listings, store them in a structured way,
and make the data accessible for non-technical users.

The project is developed step by step:
- Start with CSV as storage
- Migrate to SQLite
- Build a simple GUI using PyQt5

## Features
- Scrape job listings from websites
- Store scraped data in CSV files
- Prevent duplicate job entries
- **Structured logging** with separate files for all logs and errors
- Prepare architecture for future database integration

## Tech Stack
- Python 3.10+
- Playwright
- CSV (current storage)
- SQLite (planned)
- PyQt5 (planned)

## Project Structure
projects/
├── scraper/
├── storage/
├── services/
├── gui/
├── main.py

## Getting Started

### Prerequisites
- Python 3.10+
- Git

### Installation

1. Clone the repository:
```bash
   git clone https://github.com/thanhthien176/playwright-scraping-jobs.git
   cd playwright-scraping-jobs
```

2. Create and activate a virtual environment:
```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # Mac/Linux
```

3. Install dependencies:
```bash
   pip install -r requirements.txt
```

4. Install Playwright browsers:
```bash
   playwright install
```

## How to Run
```bash
python main.py
```

## Logging                                         
Log files are automatically created in the `logs/` directory on first run.

| File | Level | Description |
|------|-------|-------------|
| `logs/app.log` | DEBUG and above | All activities of the program |
| `logs/errors.log` | ERROR and Above | Only serious errors |

Log format:
```
2026-02-28 10:30:01 | scraper | INFO | Have scraped 20 jobs
```

> `logs/` is excluded from version control. The directory is created automatically at runtime.

## CSV
'''
job_id,title,company,location,min_salary,max_salary,url
ced00086448c2649fdb396baeba21a83,Internal HR Team Lead,CÔNG TY F&B ONSET,TP.HCM,15000000,25000000,https://example.com/internal-hr-team-lead.html
'''

## Roadmap
- [x] CSV storage
- [ ] SQLite integration
- [x] Data validation & deduplication
- [ ] PyQt5 GUI for non-technical users

## Why this project?
Many job scraping scripts are hard to maintain and extend.
This project focuses on clean architecture and gradual scalability.


