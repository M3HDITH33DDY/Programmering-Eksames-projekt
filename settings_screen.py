from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt

class SettingsScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("Settings")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        
        toggle_mode_button = QPushButton("Toggle Mode")
        toggle_mode_button.clicked.connect(self.toggle_mode)
        layout.addWidget(toggle_mode_button)
        
        self.mode_label = QLabel("Current Mode: Light")
        self.mode_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.mode_label)
        
        toggle_drag_button = QPushButton("Toggle Button Drag")
        toggle_drag_button.clicked.connect(self.toggle_drag)
        layout.addWidget(toggle_drag_button)
        
        self.drag_label = QLabel("Drag: Disabled")
        self.drag_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.drag_label)
        
        layout.addStretch()
        self.setLayout(layout)
        self.is_dark_mode = False
        self.drag_enabled = False

    def toggle_mode(self):
        self.is_dark_mode = not self.is_dark_mode
        if self.is_dark_mode:
            self.mode_label.setText("Current Mode: Dark")
            self.setStyleSheet("background-color: #333; color: white;")
        else:
            self.mode_label.setText("Current Mode: Light")
            self.setStyleSheet("")

    def toggle_drag(self):
        self.drag_enabled = not self.drag_enabled
        main_window = self.window()
        home_screen = main_window.home_screen
        home_screen.toggle_drag(self.drag_enabled)
        self.drag_label.setText(f"Drag: {'Enabled' if self.drag_enabled else 'Disabled'}")