from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QTableWidget,
    QTableWidgetItem,
    QSplitter,
    QGridLayout,
)

class TablesTab(QWidget):
    def __init__(self, row:int, column:int):
        super().__init__()
        self.row = row
        self.column = column
        
        # table
        self.tables = QTableWidget(self.row, self.column)
        
        # splitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.tables)
        
        # layout
        layout = QGridLayout()
        
        # add widget
        layout.addWidget(splitter)      
        
        self.setLayout(layout)
        
    def set_headers(self, columns: list[str]):
        if columns:
            self.tables.setHorizontalHeaderLabels(columns)
    
    def set_values(self, num_row:int, data_row):
        for i,value in enumerate(data_row):
            self.tables.setItem(num_row, i, QTableWidgetItem(value))
    
        
        
        
        
        