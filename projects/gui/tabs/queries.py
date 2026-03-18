from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSplitter,
    QTextEdit    
)
from tabs.tables import TablesTab

class QueriesTab(QWidget):
    def __init__(self):
        super().__init__()
        
        # ====LEFT PANEL=====
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        left_label = QLabel("LEFT LABEL")
        left_layout.addWidget(left_label)
        
        #=======RIGHT PANEL=======
        right_splitter = QSplitter(Qt.Vertical)
        
        right_label = QLabel("Queries: ")
        self.query = QTextEdit()
        self.table = TablesTab(5,5)
        
        right_splitter.addWidget(right_label)
        right_splitter.addWidget(self.query)
        right_splitter.addWidget(self.table)
        
        # ======MAIN SPLITTER=======
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_splitter)
        
        # =====MAIN LAYOUT=========
        layout = QHBoxLayout()
        layout.addWidget(splitter)
        
        self.setLayout(layout)
        
        
        
        
        