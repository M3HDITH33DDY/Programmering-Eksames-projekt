from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton
from PySide6.QtCore import Qt

class EditorScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("Text Editor")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)
        save_button = QPushButton("Save Text")
        save_button.clicked.connect(self.save_text)
        layout.addWidget(save_button)
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        self.setLayout(layout)

    def save_text(self):
        text = self.text_edit.toPlainText()
        with open("saved_text.txt", "w") as f:
            f.write(text)
        self.status_label.setText("Text saved to 'saved_text.txt'")