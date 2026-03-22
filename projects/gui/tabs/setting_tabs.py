from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QSpinBox,
    QPushButton,
    QGridLayout,
    QLineEdit,
    QHBoxLayout,
    QVBoxLayout,
    QTextEdit
)
class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()
        
        # thread spin
        self.thread_spin = QSpinBox()
        self.thread_spin.setMinimum(0)
        self.thread_spin.setMaximum(10)
        self.thread_spin.setValue(4)
        
        # delay spin
        self.delay_spin = QSpinBox()
        self.delay_spin.setMinimum(0)
        self.delay_spin.setMaximum(10)
        self.delay_spin.setValue(3)
        
        # save file
        self.path_edit = QLineEdit()
        self.browse_btn = QPushButton("Browse")
        
        # left layout
        grid_layout = QGridLayout()
        grid_layout.addWidget(QLabel("Thread Count: "), 0,0)
        grid_layout.addWidget(self.thread_spin, 0,1)
        grid_layout.addWidget(QLabel("Delay (sec): "), 1,0)
        grid_layout.addWidget(self.delay_spin, 1,1)
        grid_layout.addWidget(QLabel("Save Folder: "), 2,0)
        grid_layout.addWidget(self.path_edit, 2,1)
        grid_layout.addWidget(self.browse_btn, 2,2)
        
        
        
        
        # setting layout
        setting_layout = QVBoxLayout()
        setting_layout.addLayout(grid_layout)
        setting_layout.addStretch()
        
        self.setLayout(setting_layout)
        