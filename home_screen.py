from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QApplication
from PySide6.QtGui import QIcon, QDrag, QDragEnterEvent, QDropEvent
from PySide6.QtCore import Qt, QSize, QPoint, QMimeData

class DraggableButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.drag_enabled = False
        self.setFixedSize(QSize(160, 90))
        self.setStyleSheet("""
            QPushButton {
                border-radius: 45px;
                background-color: #15803D;
                color: #FFFFFF;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
                font-family: Arial, sans-serif;
            }
            QPushButton:hover {
                background-color: #16A34A;
            }
            QPushButton:pressed {
                background-color: #14532D;
            }
        """)
        self.setAcceptDrops(True)
        self.setIcon(QIcon("picture.png"))
        self.setIconSize(QSize(48, 48))
        
        # Connect the clicked signal to a handler
        self.clicked.connect(self.on_button_pressed)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton and self.drag_enabled:
            self.drag_start_position = e.pos()
        super().mousePressEvent(e)  # Ensure the clicked signal is emitted

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

    def on_button_pressed(self):
        # Action to perform when the button is pressed
        print(f"{self.text()} pressed!")

class HomeScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #1E1E1E;")
        self.layout = QVBoxLayout()
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        self.title = QLabel("Velkommen til IMV!")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            font-family: Arial, sans-serif;
            color: #D1D5DB;
            padding: 10px;
        """)
        self.layout.addWidget(self.title)
        
        # Matematik row container with label and buttons
        self.row1_container = QWidget()
        self.row1_container.setStyleSheet("background-color: #2D2D2D; border-radius: 10px;")
        self.row1_inner_layout = QVBoxLayout(self.row1_container)
        self.row1_inner_layout.setSpacing(10)
        self.matematik_label = QLabel("Matematik")
        self.matematik_label.setAlignment(Qt.AlignCenter)
        self.matematik_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            font-family: Arial, sans-serif;
            color: #FFFFFF;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1E3A8A, stop:1 #3B82F6);
            border-radius: 10px;
            padding: 8px;
            letter-spacing: 1px;
        """)
        self.row1_inner_layout.addWidget(self.matematik_label)
        
        self.row1_button_layout = QHBoxLayout()
        self.row1_button_layout.setSpacing(30)
        self.row1_button_layout.setAlignment(Qt.AlignCenter)
        self.row1_inner_layout.addLayout(self.row1_button_layout)
        
        # Kemi row container with label and buttons
        self.row2_container = QWidget()
        self.row2_container.setStyleSheet("background-color: #2D2D2D; border-radius: 10px;")
        self.row2_inner_layout = QVBoxLayout(self.row2_container)
        self.row2_inner_layout.setSpacing(10)
        self.kemi_label = QLabel("Kemi")
        self.kemi_label.setAlignment(Qt.AlignCenter)
        self.kemi_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            font-family: Arial, sans-serif;
            color: #FFFFFF;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #14532D, stop:1 #22C55E);
            border-radius: 10px;
            padding: 8px;
            letter-spacing: 1px;
        """)
        self.row2_inner_layout.addWidget(self.kemi_label)
        
        self.row2_button_layout = QHBoxLayout()
        self.row2_button_layout.setSpacing(30)
        self.row2_button_layout.setAlignment(Qt.AlignCenter)
        self.row2_inner_layout.addLayout(self.row2_button_layout)
        
        self.buttons = [
            DraggableButton(f"Button {i+1}", self) for i in range(6)
        ]
        image_paths = ["image1.png", "image2.png", "image3.png", "image4.png", "image5.png", "image6.png"]
        for i, button in enumerate(self.buttons):
            button.setIcon(QIcon(image_paths[i]))
        
        for i in range(3):
            self.row1_button_layout.addWidget(self.buttons[i])
        for i in range(3, 6):
            self.row2_button_layout.addWidget(self.buttons[i])
        
        self.layout.addWidget(self.row1_container)
        self.layout.addWidget(self.row2_container)
        self.layout.addStretch()
        self.setLayout(self.layout)
        
    def toggle_drag(self, enabled):
        for button in self.buttons:
            button.set_drag_enabled(enabled)

# Example usage
if __name__ == "__main__":
    app = QApplication([])
    window = HomeScreen()
    window.show()
    app.exec()