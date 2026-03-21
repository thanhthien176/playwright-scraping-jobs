"""
    Scraper tabs in UI
"""
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QComboBox,
    QProgressBar,
    QTextEdit
    )

class ScraperTab(QWidget):
    def __init__(self):
        super().__init__()
        
        # url input
        self.url_combo = QComboBox()
        self.url_combo.insertItem(0, "Select")
        
        # input layout
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("URL: "))
        input_layout.addWidget(self.url_combo)
        
        # button
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        self.clear_button = QPushButton("Clear")
        
        # set enabled
        self.stop_button.setEnabled(False)
        self.clear_button.setEnabled(False)
        
        # button layout
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.start_button)
        btn_layout.addWidget(self.stop_button)
        btn_layout.addStretch()
        btn_layout.addWidget(self.clear_button)        
        
        # progress bar
        self.progress = QProgressBar()
        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        self.progress.setValue(30)
        
        # Log box
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        
        # scraper layout
        scraper_layout = QVBoxLayout()
        scraper_layout.addLayout(input_layout)
        scraper_layout.addLayout(btn_layout)
        scraper_layout.addWidget(self.progress)
        scraper_layout.addWidget(self.log_box)
        scraper_layout.setSpacing(10)
        scraper_layout.setContentsMargins(20,20,20,20)
        
        # set layout
        self.setLayout(scraper_layout)
        
        # add event
        self.start_button.clicked.connect(self.start_scraping)
        self.stop_button.clicked.connect(self.stop_scraping)
        self.clear_button.clicked.connect(self.clear_log)
        
    def start_scraping(self):
        url = self.get_url()
        text = self.get_text()
        self.clear_button.setEnabled(True)
        
        if url:
            self.append_log(text=text)
            self.append_log(text=url)
            
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
        else:
            self.append_log("Please select industry")
            
    def stop_scraping(self):
        self.clear_button.setEnabled(True)
        self.log_box.append("Stop scraping")
        
        self.stop_button.setEnabled(False)
        self.start_button.setEnabled(True)
        
    def clear_log(self):
        self.clear_button.setEnabled(False)
        
        self.log_box.clear()
    
    def add_item_box(self, name:str, url:str):
        self.url_combo.addItem(name, url)
        
    def get_url(self):
        return self.url_combo.currentData()
    
    def get_text(self):
        return self.url_combo.currentText()
    
    def append_log(self, text:str):
        self.log_box.append(text)
        