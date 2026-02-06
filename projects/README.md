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
