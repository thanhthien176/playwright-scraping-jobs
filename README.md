# Job Data Scraping & Processing System

## Overview
This project is a job scraping tool built with Python and Playwright.
The goal is to collect job listings, store them in a structured way,
and make the data accessible for non-technical users.

The project is developed step by step:
- Start with CSV as storage
- Migrate to SQLite
- Build a simple GUI using PyQt5

## Features
- Automated job scraping using Playwright (handling dynamic content)
- Data pipeline: scraping → validation → storage (SQLite)
- Deduplication to prevent duplicate records
- Structured logging system (separate app & error logs)
- Modular architecture for scalability and maintainability
- Desktop GUI (PySide6) for data visualization and management

## Highlights
- Collected and processed 10000+ job records
- Reduced duplicate data entries through validation logic
- Designed system architecture for future scalability

## Tech Stack
- Python 3.10+
- Playwright
- CSV
- SQLite
- PySide6

## Project Structure
- scraper/: handles data extraction using Playwright
- storage/: database interaction (SQLite, schema, CRUD)
- services/: data processing and business logic
- controller/: coordinates workflow between components
- gui/: PySide6-based desktop interface
- config/: application settings and configuration
- threading/: background tasks for scraping and UI responsiveness
- main.py: application entry point

**The system is designed** with a modular architecture to ensure scalability, maintainability, and clear separation of concerns.

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
| `logs/app.log` | DEBUG and Higher | All activities of the program |
| `logs/errors.log` | ERROR and Higher | Only serious errors |

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
- [x] SQLite integration
- [x] Data validation & deduplication
- [x] PySide6 GUI for non-technical users

## Why this project?
Many scraping scripts are difficult to scale and maintain.
This project focuses on building a structured, modular system that can evolve from simple scripts to a scalable data processing application.


