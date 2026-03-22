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
from config.settings import WINDOW_SIZE, WINDOW_TITLE


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle(WINDOW_TITLE)
        self.resize(*WINDOW_SIZE)
        
        #tabs widget
        tabs = QTabWidget()
        self.setCentralWidget(tabs)
        
        self.scraper_tab = ScraperTab()
        self.table_tab = TablesTab(5,5)
        self.setting_tab = SettingsTab()
        self.query_tab = QueriesTab()
        
        # add tabs
        tabs.addTab(self.scraper_tab, "Scraper")
        tabs.addTab(self.table_tab, "Data")
        tabs.addTab(self.query_tab, "Query")
        tabs.addTab(self.setting_tab, "Settings")
        
        
        #status bar
        self.status = self.statusBar()
        
        self.status.showMessage('Ready')

        
        
