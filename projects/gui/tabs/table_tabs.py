from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QTableWidget,
    QTableWidgetItem,
    QSplitter,
    QGridLayout,
)

class TablesTab(QWidget):
    def __init__(self):
        super().__init__()
          
        # table
        self.table = QTableWidget()
        
        # splitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.table)
        
        # layout
        layout = QGridLayout()
        
        # add widget
        layout.addWidget(splitter)      
        
        self.setLayout(layout)
    
    def set_table_headers(self, headers: list):
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
    
    def load_data_to_table(self, headers: list, data_rows: list[dict]):
        self.table.setRowCount(len(data_rows))
        
        for row, item in enumerate(data_rows):
            for col, key in enumerate(headers):
                self.tables.setItem(
                    row, col, QTableWidgetItem(str(item.get(key, "")))
                )
        
        self.table.resizeColumnsToContents()
    
    def add_row(self, headers:list, data: dict):
        row = self.table.rowCount()
        self.table.insertRow(row)
        for col, key in enumerate(headers):
            self.table.setItem(
                row, col,
                QTableWidgetItem(str(data.get(key, '')))
            )
        
    def table_clear(self):
        self.table.clear()
