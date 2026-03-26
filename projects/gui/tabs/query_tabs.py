from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSplitter,
    QTextEdit,
    QPushButton,
    QTreeWidget,
    QTreeWidgetItem,
    QTableView    
)
from .table_views.table_model import DynamicTableModel
class QueriesTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        
        # ====LEFT PANEL=====
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        self.tree = QTreeWidget()
        left_layout.addWidget(self.tree)
        
        #=======RIGHT PANEL=======
        right_splitter = QSplitter(Qt.Vertical)
        
        right_label = QLabel("Queries: ")
        self.query = QTextEdit()
        
        # table view model
        self.model = DynamicTableModel()
        self.table = QTableView()
        self.table.setModel(self.model)
        
        #======BUTTON LAYOUT======
        self.query_btn = QPushButton("Query")
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.query_btn)
        btn_widget = QWidget()
        btn_widget.setLayout(btn_layout)
        
        # SET RIGHT PANEL
        right_splitter.addWidget(right_label)
        right_splitter.addWidget(self.query)
        right_splitter.addWidget(btn_widget)
        right_splitter.addWidget(self.table)
        
        # ======MAIN SPLITTER=======
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_splitter)
        
        # =====MAIN LAYOUT=========
        layout = QHBoxLayout()
        layout.addWidget(splitter)
        
        self.setLayout(layout)
        
        self.tree.itemClicked.connect(self.on_item_click)
    
    def load_data_to_table(self, rows: list[dict], columns:list[str], headers:dict[str, str]):
        success, message = self.model.load(rows=rows, columns=columns, headers=headers)
        return success, message
    
    
    def on_item_click(self, item:QTreeWidgetItem, column:int):
        if item:
            table_name = item.text(0)
            schemas = item.data(0,Qt.UserRole)
            if schemas:
                self.main_window.start_query(table_name, schemas=schemas)
        
        
    def build_tree(self, table_schema):
        """Build tree tables and schemas

        Args:
            table_schema (dict): {
                table_name: schema
            }
        """
        self.table_schema = table_schema
        root = QTreeWidgetItem(["Tables"])
        self.tree.addTopLevelItem(root)
        
        if self.table_schema:
        
            for table, schemas in self.table_schema.items():
                item = QTreeWidgetItem(root, [table])
                
                schema_items = [QTreeWidgetItem([item]) for item in schemas]
                
                item.addChildren(schema_items)
                
                item.setData(0, Qt.UserRole, schemas)
                
                item.setExpanded(True)
            
            root.setExpanded(True)
            self.tree.setColumnWidth(0,300)
                
            
            
              
        
        
        