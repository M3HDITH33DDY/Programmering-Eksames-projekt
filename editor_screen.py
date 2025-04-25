import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QFileDialog
from PySide6.QtCore import Qt

class EditorScreen(QWidget):
    """En teksteditor til at skrive, gemme, indlæse og oprette nye tekstfiler i en mørk-tema brugergrænseflade."""

    def __init__(self):
        super().__init__()
        # Set dark mode stylesheet
        self.setStyleSheet("""
            QWidget {
                background-color: #1F2937;
                color: #F9FAFB;
                font-family: Arial, sans-serif;
            }
            QTextEdit {
                background-color: #374151;
                color: #F9FAFB;
                border: 1px solid #4B5563;
                border-radius: 8px;
                padding: 8px;
                font-family: Consolas, monospace;
                font-size: 14px;
            }
        """)

        # Main layout with consistent margins and spacing
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Title label
        label = QLabel("Teksteditor")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #F9FAFB;
            padding: 10px;
        """)
        layout.addWidget(label)

        # Text editor
        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        # New file button
        new_button = QPushButton("Ny Fil")
        new_button.setFixedHeight(40)
        new_button.setStyleSheet("""
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
        new_button.clicked.connect(self.new_file)
        layout.addWidget(new_button)

        # Save button
        save_button = QPushButton("Gem Tekst")
        save_button.setFixedHeight(40)
        save_button.setStyleSheet("""
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
        save_button.clicked.connect(self.save_text)
        layout.addWidget(save_button)

        # Load button
        load_button = QPushButton("Indlæs Tekst")
        load_button.setFixedHeight(40)
        load_button.setStyleSheet("""
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
        load_button.clicked.connect(self.load_text)
        layout.addWidget(load_button)

        # Status label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            font-size: 14px;
            color: #D1D5DB;
            padding: 5px;
        """)
        layout.addWidget(self.status_label)

        self.setLayout(layout)
        self.current_file = None  # Track the currently loaded file

    def new_file(self):
        """
        Opretter en ny tekstfil ved at rydde teksteditoren og nulstille den aktuelle fil.
        """
        self.text_edit.clear()
        self.current_file = None
        self.status_label.setText("Ny fil oprettet")

    def save_text(self):
        """
        Gemmer teksteditorens indhold til den aktuelt indlæste fil eller en ny fil.

        Hvis en fil er indlæst, overskrives den; ellers åbnes en fildialog for at vælge filnavn.
        Viser kun filnavnet i statusbeskeden.
        """
        text = self.text_edit.toPlainText()
        if self.current_file:
            try:
                with open(self.current_file, "w", encoding="utf-8") as f:
                    f.write(text)
                file_name = os.path.basename(self.current_file)
                self.status_label.setText(f"Tekst gemt til '{file_name}'")
            except Exception as e:
                self.status_label.setText(f"Fejl ved gemning: {str(e)}")
        else:
            file_name, _ = QFileDialog.getSaveFileName(self, "Gem Tekst", "", "Text Files (*.txt);;All Files (*)")
            if file_name:
                try:
                    with open(file_name, "w", encoding="utf-8") as f:
                        f.write(text)
                    self.current_file = file_name
                    display_name = os.path.basename(file_name)
                    self.status_label.setText(f"Tekst gemt til '{display_name}'")
                except Exception as e:
                    self.status_label.setText(f"Fejl ved gemning: {str(e)}")
            else:
                self.status_label.setText("Gemning annulleret")

    def load_text(self):
        """
        Indlæser tekst fra en brugerdefineret fil og viser den i teksteditoren.

        Åbner en fildialog for at vælge en tekstfil; opdaterer den aktuelle fil og viser kun filnavnet i statusbeskeden.
        """
        file_name, _ = QFileDialog.getOpenFileName(self, "Indlæs Tekst", "", "Text Files (*.txt);;All Files (*)")
        if file_name:
            try:
                with open(file_name, "r", encoding="utf-8") as f:
                    text = f.read()
                self.text_edit.setPlainText(text)
                self.current_file = file_name
                display_name = os.path.basename(file_name)
                self.status_label.setText(f"Tekst indlæst fra '{display_name}'")
            except Exception as e:
                self.status_label.setText(f"Fejl ved indlæsning: {str(e)}")
        else:
            self.status_label.setText("Indlæsning annulleret")