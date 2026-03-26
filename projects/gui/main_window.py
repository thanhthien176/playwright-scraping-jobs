import sys
from PySide6.QtWidgets import (
    QMainWindow,
    QTabWidget,
    QStatusBar,
)
from .tabs.scraper_tabs import ScraperTab
from .tabs.table_tabs import TablesTab
from .tabs.setting_tabs import SettingsTab
from .tabs.query_tabs import QueriesTab
from controllers.scraper_controller import ScrapeController
from config.settings import WINDOW_SIZE, WINDOW_TITLE


class MainWindow(QMainWindow):
    def __init__(self, writer):
        super().__init__()
        
        self.setWindowTitle(WINDOW_TITLE)
        self.resize(*WINDOW_SIZE)
        
        #tabs widget
        tabs = QTabWidget()
        self.setCentralWidget(tabs)
        
        self.scraper_tab = ScraperTab(main_window=self)
        self.table_tab = TablesTab()
        self.setting_tab = SettingsTab()
        self.query_tab = QueriesTab(main_window=self)
        
        # add tabs
        tabs.addTab(self.scraper_tab, "Scraper")
        tabs.addTab(self.table_tab, "Data")
        tabs.addTab(self.query_tab, "Query")
        tabs.addTab(self.setting_tab, "Settings")
        
        #status bar
        self.status = self.statusBar()
        
        self.status.showMessage('Ready')
        self.controller = ScrapeController(window=self, writer=writer)
        
        
    def update_tree(self, table_schema:dict):
        if table_schema:
            self.query_tab.build_tree(table_schema)
        
    def update_table_view(self, rows:list[dict], headers:dict[str, str]|None = None):
        columns = self.columns if self.columns else []
        success, message = self.query_tab.load_data_to_table(rows=rows, columns=columns, headers=headers)

        if not success:
            self.append_log_box("Error: {message}")
        return success 
    
    def start_query(self, table_name, schemas):
        self.columns = schemas
        self.controller.load_data_to_ui(table_name=table_name)
        
    def start_scraping(self):
        self.controller.start_scraping()
    
    def stop_scraping(self):
        self.controller.stop_scraping()
        
    def append_log_box(self, text):
        self.scraper_tab.append_log(text)
    
    def update_status(self, text:str):
        self.status.showMessage(text)
    
    # Get dict industry from QComboBox in scraper_tab    
    def get_industry(self):
        return self.scraper_tab.get_industry()
    
    # Set headers for table to show data was scraped
    def set_table_tab_headers(self, headers):
        self.table_tab.set_table_headers(headers)
    
    # add data into a row of the table
    def add_table_row(self, headers, data):
        self.table_tab.add_row(headers=headers, data=data)
    
    # Set text and data for QComboBox
    def add_item_box(self, industry):
        self.scraper_tab.add_item_box(data=industry)

    # set button in scraper_tab
    def set_button_stop(self):
        self.scraper_tab.set_button_stop()
