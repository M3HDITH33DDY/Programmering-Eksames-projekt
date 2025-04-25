import json
import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QApplication, QMenu
from PySide6.QtGui import QIcon, QDrag, QDragEnterEvent, QDropEvent, QAction
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
                box-shadow: 1px 1px 4px rgba(0, 0, 0, 0.5);
            }
            QPushButton:hover {
                background-color: #16A34A;
                box-shadow: 0 0 8px rgba(22, 163, 74, 0.5);
            }
        """)
        self.setAcceptDrops(True)
        self.setIcon(QIcon("picture.png"))
        self.setIconSize(QSize(48, 48))
        self.screen_key = None  # Store the associated screen key (e.g., "formulacollection")

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton and self.drag_enabled:
            self.drag_start_position = e.pos()
        elif e.button() == Qt.RightButton:
            self.show_context_menu(e.pos())
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
            # Swap button configurations
            source_text, source_screen_key = source.text(), source.screen_key
            self_text, self_screen_key = self.text(), self.screen_key
            source.setText(self_text)
            source.screen_key = self_screen_key
            self.setText(source_text)
            self.screen_key = source_screen_key
            # Notify parent to save configuration
            self.parentaguester(self.parent(), HomeScreen).save_button_config()
            e.acceptProposedAction()

    def set_drag_enabled(self, enabled):
        self.drag_enabled = enabled

    def show_context_menu(self, pos):
        menu = QMenu(self)
        screens = [
            ("Formelsamling", "formulacollection"),
            ("Entalpi Beregner", "enthalpy"),
            ("Graph War", "game"),
            ("Text Editor", "editor"),
            ("PDF Viewer", "pdf_viewer"),
            ("Settings", "settings")
        ]
        for label, key in screens:
            action = QAction(label, self)
            action.setData(key)
            action.triggered.connect(lambda: self.assign_screen(action.data()))
            menu.addAction(action)
        menu.exec(self.mapToGlobal(pos))

    def assign_screen(self, screen_key):
        self.screen_key = screen_key
        # Update button text based on screen key
        screen_labels = {
            "formulacollection": "Formelsamling",
            "enthalpy": "Entalpi Beregner",
            "game": "Graph War",
            "editor": "Text Editor",
            "pdf_viewer": "PDF Viewer",
            "settings": "Settings"
        }
        self.setText(screen_labels.get(screen_key, "Unassigned"))
        # Save configuration
        self.parent().save_button_config()

class HomeScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window  # Reference to MainWindow for screen switching
        self.setStyleSheet("background-color: #1E1E1E;")
        self.layout = QVBoxLayout()
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        self.title = QLabel("Welcome to IMV")
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
            box-shadow: 1px 1px 4px rgba(0, 0, 0, 0.5);
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
            box-shadow: 1px 1px 4px rgba(0, 0, 0, 0.5);
        """)
        self.row2_inner_layout.addWidget(self.kemi_label)
        
        self.row2_button_layout = QHBoxLayout()
        self.row2_button_layout.setSpacing(30)
        self.row2_button_layout.setAlignment(Qt.AlignCenter)
        self.row2_inner_layout.addLayout(self.row2_button_layout)
        
        self.buttons = [DraggableButton("Unassigned", self) for _ in range(6)]
        for i, button in enumerate(self.buttons):
            button.clicked.connect(lambda checked, idx=i: self.button_clicked(idx))
        
        # Load button configuration
        self.load_button_config()
        
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
    
    def load_button_config(self):
        config_file = "button_config.json"
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                for idx, data in config.items():
                    idx = int(idx)
                    if idx < len(self.buttons):
                        self.buttons[idx].setText(data.get("label", "Unassigned"))
                        self.buttons[idx].screen_key = data.get("screen_key")
            except Exception as e:
                print(f"Error loading button config: {str(e)}")
    
    def save_button_config(self):
        config = {}
        for idx, button in enumerate(self.buttons):
            config[idx] = {
                "label": button.text(),
                "screen_key": button.screen_key
            }
        try:
            with open("button_config.json", 'w') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            print(f"Error saving button config: {str(e)}")
    
    def button_clicked(self, button_idx):
        button = self.buttons[button_idx]
        if button.screen_key:
            screen_map = {
                "formulacollection": self.main_window.formulacollection_screen,
                "enthalpy": self.main_window.enthalpy_screen,
                "game": self.main_window.game_screen,
                "editor": self.main_window.editor_screen,
                "pdf_viewer": self.main_window.pdf_viewer_screen,
                "settings": self.main_window.settings_screen
            }
            screen = screen_map.get(button.screen_key)
            if screen:
                self.main_window.stacked_widget.setCurrentWidget(screen)