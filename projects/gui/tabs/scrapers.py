"""
    Scraper tabs in UI
"""
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QProgressBar,
    QTextEdit
    )

class ScraperTab(QWidget):
    def __init__(self):
        super().__init__()
        
        # url input
        self.url_input = QLineEdit()
        
        # input layout
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("URL: "))
        input_layout.addWidget(self.url_input)
        
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
        url = self.url_input.text()
        self.clear_button.setEnabled(True)
        
        if url:
            self.log_box.append(url)
            
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
        else:
            self.log_box.append("Please enter url")
            
    def stop_scraping(self):
        self.clear_button.setEnabled(True)
        self.log_box.append("Stop scraping")
        
        self.stop_button.setEnabled(False)
        self.start_button.setEnabled(True)
        
    def clear_log(self):
        self.clear_button.setEnabled(False)
        
        self.log_box.clear()
        
        
        