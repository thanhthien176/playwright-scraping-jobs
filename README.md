# Job Scraping Tool

## Overview
This project is a job scraping tool built with Python and Playwright.
The goal is to collect job listings, store them in a structured way,
and make the data accessible for non-technical users.

The project is developed step by step:
- Start with CSV as storage
- Migrate to PostgreSQL
- Build a simple GUI using PyQt5

## Features
- Scrape job listings from websites
- Store scraped data in CSV files
- Prevent duplicate job entries
- **Structured logging** with separate files for all logs and errors
- Prepare architecture for future database integration

## Tech Stack
- Python
- Playwright
- CSV (temporary storage)
- PostgreSQL (planned)
- PyQt5 (planned)

## Project Structure
project/
├── scraper/
├── storage/
├── services/
├── gui/
├── main.py


## How to Run
1. Install dependencies
2. Run the scraper
3. Check output CSV files

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



## Roadmap
- [x] CSV storage
- [ ] PostgreSQL integration
- [ ] Data validation & deduplication
- [ ] PyQt5 GUI for non-technical users
