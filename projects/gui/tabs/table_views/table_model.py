from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QColor
import logging
from config.logging_config import setup_logging

setup_logging()
logger = logging.getLogger("table_model")

class DynamicTableModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self._rows = []
        self._columns = []
        self._headers = {}
        
    def rowCount(self, parent = QModelIndex()):
        if parent.isValid():
            return 0
        return len(self._rows)
    
    def columnCount(self, parent = QModelIndex()):
        if parent.isValid():
            return 0
        return len(self._columns)
    
    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        
        row = self._rows[index.row()]
        key = self._columns[index.column()]
        value = row.get(key)
        
        if role == Qt.DisplayRole:
            if value is None:
                return ""
            return str(value)
            
        if role == Qt.TextAlignmentRole:
            if isinstance(value, (int, float)):
                return Qt.AlignRight | Qt.AlignVCenter
            return Qt.AlignLeft | Qt.AlignVCenter
        
        if role == Qt.BackgroundRole:
            if index.row()%2 == 0:
                return QColor("#F3E3D0")
            else:
                return QColor("#D2C4B4")
        
        return None
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            key = self._columns[section]
            
            return self._headers.get(key, key)
        
        if orientation == Qt.Vertical:
            return str(section+1)
        return None
    
    def load(self, rows: list[dict], columns: list[str], headers: dict[str,str]):
        """_summary_

        Args:
            rows (list[dict]): The query result -> list[dict]
            columns (list[str]): The keys you want to display, in the order you want
            headers (dict[str,str]): Custom display name e.g., {"score": "Average Score"}
        """
        try:
            self.beginResetModel()
            if not rows:
                raise ValueError("Invalid Data")
                
            self._rows = rows
            self._columns = list(columns)
            self._headers = headers or {}
            logger.info("Loaded data into the table view success!")
            
            self.endResetModel()
            return True, "Success"
        except Exception as e:
            logger.exception("Error loading data into table view")
            return False, str(e)
        