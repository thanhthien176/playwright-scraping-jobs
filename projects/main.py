import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow
from controllers.scraper_controller import ScrapeController
from config.logging_config import setup_logging
import logging


setup_logging()
logger = logging.getLogger("main")
    
def main():
    app = QApplication(sys.argv)
    
    window = MainWindow()
    
    scraper_controller = ScrapeController(window=window)
    
    window.show()
    
    sys.exit(app.exec())
                



if __name__ == "__main__":
    main()