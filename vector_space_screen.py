import numpy as np
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton,
    QRadioButton, QTextEdit, QGroupBox
)
from PySide6.QtCore import Qt

class VectorCalculator(QWidget):
    def __init__(self):
        super().__init__()

        # Main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Coordinate input for first vector/point
        self.group1 = QGroupBox("Coordinate 1")
        group1_layout = QVBoxLayout()
        self.group1.setLayout(group1_layout)

        self.coord1_inputs = []
        coord1_layout = QHBoxLayout()
        for label in ['X:', 'Y:', 'Z:']:
            lbl = QLabel(label)
            input_field = QLineEdit()
            input_field.setPlaceholderText("0.0")
            coord1_layout.addWidget(lbl)
            coord1_layout.addWidget(input_field)
            self.coord1_inputs.append(input_field)
        group1_layout.addLayout(coord1_layout)

        # Radio buttons for vector/point
        self.vector1_radio = QRadioButton("Vector")
        self.point1_radio = QRadioButton("Point")
        self.vector1_radio.setChecked(True)
        radio1_layout = QHBoxLayout()
        radio1_layout.addWidget(self.vector1_radio)
        radio1_layout.addWidget(self.point1_radio)
        group1_layout.addLayout(radio1_layout)
        main_layout.addWidget(self.group1)

        # Coordinate input for second vector/point
        self.group2 = QGroupBox("Coordinate 2")
        group2_layout = QVBoxLayout()
        self.group2.setLayout(group2_layout)

        self.coord2_inputs = []
        coord2_layout = QHBoxLayout()
        for label in ['X:', 'Y:', 'Z:']:
            lbl = QLabel(label)
            input_field = QLineEdit()
            input_field.setPlaceholderText("0.0")
            coord2_layout.addWidget(lbl)
            coord2_layout.addWidget(input_field)
            self.coord2_inputs.append(input_field)
        group2_layout.addLayout(coord2_layout)

        # Radio buttons for vector/point
        self.vector2_radio = QRadioButton("Vector")
        self.point2_radio = QRadioButton("Point")
        self.vector2_radio.setChecked(True)
        radio2_layout = QHBoxLayout()
        radio2_layout.addWidget(self.vector2_radio)
        radio2_layout.addWidget(self.point2_radio)
        group2_layout.addLayout(radio2_layout)
        main_layout.addWidget(self.group2)

        # Calculation buttons
        button_layout = QHBoxLayout()
        operations = ["Add", "Subtract", "Dot Product", "Cross Product"]
        self.buttons = {}
        for op in operations:
            btn = QPushButton(op)
            btn.clicked.connect(lambda checked, operation=op: self.calculate(operation))
            button_layout.addWidget(btn)
            self.buttons[op] = btn
        main_layout.addLayout(button_layout)

        # Result display
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setPlaceholderText("Calculation results will appear here...")
        main_layout.addWidget(self.result_display)

    def get_coordinates(self, inputs):
        try:
            coords = [float(inp.text()) if inp.text().strip() else 0.0 for inp in inputs]
            return np.array(coords)
        except ValueError:
            return None

    def calculate(self, operation):
        # Get coordinates
        coord1 = self.get_coordinates(self.coord1_inputs)
        coord2 = self.get_coordinates(self.coord2_inputs)

        if coord1 is None or coord2 is None:
            self.result_display.setText("Error: Please enter valid numbers for coordinates.")
            return

        # Determine types
        type1 = "Vector" if self.vector1_radio.isChecked() else "Point"
        type2 = "Vector" if self.vector2_radio.isChecked() else "Point"

        # Initialize result
        result_text = f"Operation: {operation}\n"
        result_text += f"Coordinate 1 ({type1}): {coord1}\n"
        result_text += f"Coordinate 2 ({type2}): {coord2}\n"

        # Perform calculations
        try:
            if operation == "Add":
                if type1 == "Point" and type2 == "Point":
                    result_text += "Error: Addition not allowed between two points."
                else:
                    result = coord1 + coord2
                    result_text += f"Result: {result}"
            elif operation == "Subtract":
                if type1 == "Point" and type2 == "Vector":
                    result_text += "Error: Cannot subtract vector from point."
                else:
                    result = coord1 - coord2
                    result_text += f"Result: {result}"
            elif operation == "Dot Product":
                if type1 == "Point" or type2 == "Point":
                    result_text += "Error: Dot product requires two vectors."
                else:
                    result = np.dot(coord1, coord2)
                    result_text += f"Result: {result}"
            elif operation == "Cross Product":
                if type1 == "Point" or type2 == "Point":
                    result_text += "Error: Cross product requires two vectors."
                else:
                    result = np.cross(coord1, coord2)
                    result_text += f"Result: {result}"
            else:
                result_text += "Error: Unknown operation."
        except Exception as e:
            result_text += f"Error: {str(e)}"

        self.result_display.setText(result_text)