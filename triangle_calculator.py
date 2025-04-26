from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from PySide6.QtCore import Qt
import math

class TriangleCalculator(QWidget):
    """Skærm til beregning af trekants egenskaber baseret på sider."""

    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #1E1E1E; color: #FFFFFF;")
        self.layout = QVBoxLayout()
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(15, 15, 15, 15)

        # Title
        self.title = QLabel("Trekantsberegner")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            font-family: Arial, sans-serif;
            color: #D1D5DB;
            padding: 8px;
        """)
        self.layout.addWidget(self.title)

        # Input fields for sides
        self.side_a_input = QLineEdit()
        self.side_a_input.setPlaceholderText("Side a")
        self.side_a_input.setStyleSheet("""
            background-color: #2D2D2D;
            color: #FFFFFF;
            border: 1px solid #4B5563;
            border-radius: 5px;
            padding: 5px;
            font-family: Arial, sans-serif;
        """)
        self.layout.addWidget(self.side_a_input)

        self.side_b_input = QLineEdit()
        self.side_b_input.setPlaceholderText("Side b")
        self.side_b_input.setStyleSheet("""
            background-color: #2D2D2D;
            color: #FFFFFF;
            border: 1px solid #4B5563;
            border-radius: 5px;
            padding: 5px;
            font-family: Arial, sans-serif;
        """)
        self.layout.addWidget(self.side_b_input)

        self.side_c_input = QLineEdit()
        self.side_c_input.setPlaceholderText("Side c")
        self.side_c_input.setStyleSheet("""
            background-color: #2D2D2D;
            color: #FFFFFF;
            border: 1px solid #4B5563;
            border-radius: 5px;
            padding: 5px;
            font-family: Arial, sans-serif;
        """)
        self.layout.addWidget(self.side_c_input)

        # Calculate button
        self.calculate_button = QPushButton("Beregn")
        self.calculate_button.setStyleSheet("""
            QPushButton {
                border-radius: 10px;
                background-color: #15803D;
                color: #FFFFFF;
                padding: 8px;
                font-size: 14px;
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
        self.calculate_button.clicked.connect(self.calculate_triangle)
        self.layout.addWidget(self.calculate_button)

        # Result display
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setStyleSheet("""
            background-color: #2D2D2D;
            color: #FFFFFF;
            border: 1px solid #4B5563;
            border-radius: 5px;
            padding: 5px;
            font-family: Arial, sans-serif;
        """)
        self.layout.addWidget(self.result_display)

        self.layout.addStretch()
        self.setLayout(self.layout)

    def calculate_triangle(self):
        """Beregn trekants egenskaber baseret på indtastede sider."""
        try:
            a = float(self.side_a_input.text())
            b = float(self.side_b_input.text())
            c = float(self.side_c_input.text())

            # Check for valid triangle (sum of any two sides must be greater than the third)
            if (a + b <= c) or (b + c <= a) or (a + c <= b):
                self.result_display.setText("Ugyldig trekant: Summen af to sider skal være større end den tredje.")
                return

            # Calculate perimeter
            perimeter = a + b + c

            # Calculate area using Heron's formula
            s = perimeter / 2  # Semi-perimeter
            area = math.sqrt(s * (s - a) * (s - b) * (s - c))

            # Display results
            self.result_display.setText(
                f"Omkreds: {perimeter:.2f}\n"
                f"Areal: {area:.2f}"
            )
        except ValueError:
            self.result_display.setText("Fejl: Indtast venligst gyldige tal for alle sider.")