import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow
from controllers.scraper_controller import ScrapeController
from projects.threads.write_db_thread import DataWriter
from config.settings import DB_PATH
from config.logging_config import setup_logging
import logging


setup_logging()
logger = logging.getLogger("main")
    
def main():
    app = QApplication(sys.argv)
    
    window = MainWindow()
    
    writer = DataWriter(DB_PATH)
    writer.start()
    
    scraper_controller = ScrapeController(window=window, writer = writer)
    
    window.show()
    
    exit_code = app.exec()
    
    logging.info("The application is closing...")
    logging.shutdown()
    
    sys.exit(exit_code)
                



if __name__ == "__main__":
    main()