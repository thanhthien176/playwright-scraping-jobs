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
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        
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
        self.update_button = QPushButton("Update")
        self.clear_button = QPushButton("Clear")
        
        # set enabled
        self.stop_button.setEnabled(False)
        self.clear_button.setEnabled(False)
        
        # button layout
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.start_button)
        btn_layout.addWidget(self.update_button)
        btn_layout.addStretch()
        btn_layout.addWidget(self.stop_button)
        btn_layout.addWidget(self.clear_button)        
        
        # progress bar
        self.progress = QProgressBar()

        
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
        self.clear_button.clicked.connect(self.clear_log)
        self.start_button.clicked.connect(self.start_scraping)
        self.stop_button.clicked.connect(self.stop_scraping)    
    
    def start_scraping(self):
        self.set_progress_start()
        self.start_button.setEnabled(False)
        self.update_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.main_window.start_scraping()
        
    def stop_scraping(self):
        self.set_button_stop()
        self.set_button_stop()
        self.main_window.stop_scraping()
        
    def set_button_stop(self):
        self.start_button.setEnabled(True)
        self.update_button.setEnabled(True)
        self.stop_button.setEnabled(False)
    
    def set_progress_start(self):
        self.progress.setRange(0,0)
        self.progress.setFormat("Loading...")
        
    def set_progress_stop(self):
        self.progress.setRange(0,100)
        self.progress.setValue(100)
        self.progress.setFormat("Completed")
        
    
    def clear_log(self):
        self.clear_button.setEnabled(False)
        
        self.log_box.clear()
    
    def add_item_box(self, data: dict):
        name = data.get('name')
        self.url_combo.addItem(name, data)
        
    def get_industry(self):
        return self.url_combo.currentData()
    
    def get_text(self):
        return self.url_combo.currentText()
    
    def append_log(self, text:str):
        self.clear_button.setEnabled(True)
        self.log_box.append(text)
        

        