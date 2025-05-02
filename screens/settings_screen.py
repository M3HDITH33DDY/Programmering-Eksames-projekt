from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt

class SettingsScreen(QWidget):
    """En skærm til indstillinger, der tillader brugeren at aktivere/deaktivere trækfunktion i mørk tilstand."""

    def __init__(self):
        super().__init__()
        # Darkmode stylesheet
        self.setStyleSheet("""
            QWidget {
                background-color: #1F2937;
                color: #F9FAFB;
                font-family: Arial, sans-serif;
            }
        """)

        # Main layout med margins og spacing
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Titel
        title_label = QLabel("Indstillinger")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #F9FAFB;
            padding: 10px;
        """)
        layout.addWidget(title_label)

        # Knap for toogle af drag
        toggle_drag_button = QPushButton("Skift Træk")
        toggle_drag_button.setFixedHeight(40)
        toggle_drag_button.setStyleSheet("""
            QPushButton {
                background-color: #2DD4BF;
                color: #1F2937;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                padding: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #5EEAD4;
            }
            QPushButton:pressed {
                background-color: #14B8A6;
            }
        """)
        toggle_drag_button.clicked.connect(self.toggle_drag)
        layout.addWidget(toggle_drag_button)

        # Staus for drag-funktion
        self.drag_label = QLabel("Træk: Deaktiveret")
        self.drag_label.setAlignment(Qt.AlignCenter)
        self.drag_label.setStyleSheet("""
            font-size: 14px;
            color: #D1D5DB;
            padding: 5px;
        """)
        layout.addWidget(self.drag_label)

        # Tilføjelse af strech, for at skabe afstand i mellem layout
        layout.addStretch()
        self.setLayout(layout)

        # Initialisering af stadie for drag
        self.drag_enabled = False

    def toggle_drag(self):
        """
        Aktiverer eller deaktiverer trækfunktionen for knapper på hjemmeskærmen.

        Opdaterer hovedvinduet og statuslabel for at afspejle træktilstanden.
        """
        self.drag_enabled = not self.drag_enabled
        main_window = self.window()
        home_screen = main_window.home_screen
        home_screen.toggle_drag(self.drag_enabled)
        self.drag_label.setText(f"Træk: {'Aktiveret' if self.drag_enabled else 'Deaktiveret'}")