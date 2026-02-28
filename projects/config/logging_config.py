import logging
import logging.config
from pathlib import Path

# Create logs folder if it's existed
Path("logs").mkdir(exist_ok=True)

LOGGING_CONFIG ={
    "version": 1,
    "disable_existing_loggers": False,
    
    "formatters":{
        "detailed": {
            "format": "%(asctime)s | %(name)-15s | %(levelname)-8s | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "simple":{
            "format": "%(levelname)s | $(message)s"
        }
    },
    
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "level": "INFO"
        },
        "file_all": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/app.log",
            "formatter": "detailed",
            "level": "DEBUG",
            "maxBytes": 5_000_000,
            "backupCount": 3,
            "encoding": "utf-8"
        },
        "file_errors": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/errors.log",
            "formatter": "detailed",
            "level": "ERROR",
            "maxBytes": 2_000_000,
            "backupCount": 3,
            "encoding": "utf-8"
                 
        },
    },
    
    "loggers": {
        "asyncio":{
            "level": "WARNING",
            "propagate": False,  
        },
        "scraper": {
            "level": "DEBUG",
            "handlers": ["console", "file_all", "file_errors"],
            "propagate": False,
        },
        "storage":{
            "level": "INFO",
            "handlers": ["console", "file_all", "file_errors"],
            "propagate": False,
        },
        "services": {
            "level": "INFO",
            "handlers": ["console", "file_all", "file_errors"],
            "propagate": False,
        },
    },
    
    "root": {
        "level": "DEBUG",
        "handlers": ["file_all", "file_errors"]
    }
}

def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)