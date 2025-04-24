from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QApplication
from PySide6.QtGui import QIcon, QDrag, QDragEnterEvent, QDropEvent, QAction
from PySide6.QtCore import Qt, QSize, QPoint, QMimeData

class DraggableButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.drag_enabled = False
        self.setFixedSize(QSize(150, 80))
        self.setStyleSheet("""
            QPushButton {
                border-radius: 40px;
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.setAcceptDrops(True)
        self.setIcon(QIcon("picture.png"))
        self.setIconSize(QSize(40, 40))

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton and self.drag_enabled:
            self.drag_start_position = e.pos()
        super().mousePressEvent(e)

    def mouseMoveEvent(self, e):
        if not (e.buttons() & Qt.LeftButton) or not self.drag_enabled:
            return
        if (e.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
        drag = QDrag(self)
        mime = QMimeData()
        drag.setMimeData(mime)
        drag.exec(Qt.MoveAction)

    def dragEnterEvent(self, e: QDragEnterEvent):
        if self.drag_enabled and isinstance(e.source(), DraggableButton):
            e.acceptProposedAction()

    def dropEvent(self, e: QDropEvent):
        if not self.drag_enabled:
            return
        source = e.source()
        if source != self and isinstance(source, DraggableButton):
            source_pos = source.pos()
            self_pos = self.pos()
            source.move(self_pos)
            self.move(source_pos)
            e.acceptProposedAction()

    def set_drag_enabled(self, enabled):
        self.drag_enabled = enabled

class HomeScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        
        self.title = QLabel("Welcome to the Home Screen!")
        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title)
        
        self.row1_container = QWidget()
        self.row1_layout = QHBoxLayout(self.row1_container)
        self.row1_layout.setSpacing(20)
        
        self.row2_container = QWidget()
        self.row2_layout = QHBoxLayout(self.row2_container)
        self.row2_layout.setSpacing(20)
        
        self.buttons = [
            DraggableButton(f"Button {i+1}", self) for i in range(6)
        ]
        image_paths = ["image1.png", "image2.png", "image3.png", "image4.png", "image5.png", "image6.png"]
        for i, button in enumerate(self.buttons):
            button.setIcon(QIcon(image_paths[i]))
        
        for i in range(3):
            self.row1_layout.addWidget(self.buttons[i])
        for i in range(3, 6):
            self.row2_layout.addWidget(self.buttons[i])
        
        self.layout.addWidget(self.row1_container)
        self.layout.addWidget(self.row2_container)
        self.layout.addStretch()
        self.setLayout(self.layout)
        
    def toggle_drag(self, enabled):
        for button in self.buttons:
            button.set_drag_enabled(enabled)