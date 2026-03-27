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
    QTableView,
    QHeaderView    
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
        
        self.query = QTextEdit()
        
         #======BUTTON LAYOUT======
        self.query_btn = QPushButton("Query")
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.query_btn)
        
        # right_layout
        query_layout = QVBoxLayout()
        query_layout.addWidget(QLabel("Query: "))
        query_layout.addWidget(self.query)
        query_layout.addLayout(btn_layout)
        query_layout.setContentsMargins(0,0,0,0)
        
        query_widget = QWidget()
        query_widget.setLayout(query_layout)
        
        # table view model
        self.model = DynamicTableModel()
        self.table = QTableView()
        self.table.setModel(self.model)
        
        self.table.setAlternatingRowColors(True)
        # Set columns size
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)
        self.table.resizeColumnsToContents()
        header.setStretchLastSection(True)
        
        # SET RIGHT PANEL
        right_splitter.addWidget(query_widget)
        right_splitter.addWidget(self.table)
        right_splitter.setCollapsible(0, False)

        
        # ======MAIN SPLITTER=======
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_splitter)
        splitter.setSizes([200, 800])
        splitter.setStretchFactor(0,0)
        splitter.setStretchFactor(1,1)
        
        
        # =====MAIN LAYOUT=========
        layout = QHBoxLayout()
        layout.addWidget(splitter)
        layout.setContentsMargins(20,20,10,15)        
        
        self.setLayout(layout)
        
        self.tree.itemClicked.connect(self.on_item_click)
        self.query_btn.clicked.connect(self.safe_query)

        
    def safe_query(self):
        query_text = self.query.toPlainText()
        self.main_window.safe_query(query_text)
    
    def load_data_to_table(self, rows: list[dict], columns:list[str], headers:dict[str, str]):
        success, message = self.model.load(rows=rows, columns=columns, headers=headers)
        return success, message
    
    
    def on_item_click(self, item:QTreeWidgetItem, column:int):
        if item:
            table_name = item.text(0)
            schemas = item.data(0,Qt.UserRole)
            if schemas:
                self.main_window.start_select(table_name)
        
        
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
                
            
            
              
        
        
        