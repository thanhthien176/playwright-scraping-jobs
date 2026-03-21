import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
    QStatusBar,
)
from tabs.scrapers import ScraperTab
from tabs.tables import TablesTab
from tabs.settings import SettingsTab
from tabs.queries import QueriesTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Scraper App")
        self.resize(700,500)
        
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
        self.statusBar().showMessage("Ready")
        
        
    


def main():
    app = QApplication(sys.argv)
    
    window = MainWindow()
    
    window.show()
    
    sys.exit(app.exec())
    
    
if __name__ == "__main__":
    main()