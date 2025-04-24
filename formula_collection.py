from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class FormulaCollectionScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("Formelsamling")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.mode_label = QLabel("Test x⁴")
        self.mode_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.mode_label)
        layout.addStretch()
        self.setLayout(layout)