# config/settings.py

# ===== DATABASE =====
DB_PATH = "database/scraper.db"

# ===== DATA =====
DATA_DIR = "data/"
RAW_DATA_DIR = "data/raw/"
PROCESSED_DATA_DIR = "data/processed/"

# ===== LOG =====
LOG_FILE = "logs/app.log"
ERROR_LOG_FILE = "logs/errors.log"

# ===== SCRAPER =====
TIMEOUT = 2000
BASE_URL = "https://example.com"

# ===== UI =====
WINDOW_TITLE = "Scraper App"
WINDOW_SIZE = (700, 500)

#====== TABLE ======
HEADER_JOB = ['job_id', 'title', 'company', 'location', 'min_salary', 'max_salary', 'url', 'industry_id']