import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow
from controllers.scraper_controller import ScrapeController
from threads.write_db_thread import DataWriter
from config.settings import DB_PATH
from config.logging_config import setup_logging
import logging


setup_logging()
logger = logging.getLogger("main")
    
def main():
    app = QApplication(sys.argv)
        
    writer = DataWriter(DB_PATH)
    writer.start()
    db = writer.db
    
    window = MainWindow(writer)
    
    
    tables = db.tables()
    table_schema = {}
    for table in tables:
        table_name = table.get("name")
        if table_name:
            table_schema[table_name] = db.schema(table_name).keys()
    
    window.update_tree(table_schema)
    
    scraper_controller = ScrapeController(window=window, writer = writer)
    
    window.show()
    
    
    exit_code = app.exec()
    
    logging.info("The application is closing...")
    logging.shutdown()
    
    sys.exit(exit_code)
                



if __name__ == "__main__":
    main()