import numpy as np
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton,
    QRadioButton, QTextEdit, QGroupBox
)
from PySide6.QtCore import Qt
from vector_calculations import VectorOperations

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

        # Coordinate input for third vector/point
        self.group3 = QGroupBox("Coordinate 3")
        group3_layout = QVBoxLayout()
        self.group3.setLayout(group3_layout)

        self.coord3_inputs = []
        coord3_layout = QHBoxLayout()
        for label in ['X:', 'Y:', 'Z:']:
            lbl = QLabel(label)
            input_field = QLineEdit()
            input_field.setPlaceholderText("0.0")
            coord3_layout.addWidget(lbl)
            coord3_layout.addWidget(input_field)
            self.coord3_inputs.append(input_field)
        group3_layout.addLayout(coord3_layout)

        # Radio buttons for vector/point
        self.vector3_radio = QRadioButton("Vector")
        self.point3_radio = QRadioButton("Point")
        self.vector3_radio.setChecked(True)
        radio3_layout = QHBoxLayout()
        radio3_layout.addWidget(self.vector3_radio)
        radio3_layout.addWidget(self.point3_radio)
        group3_layout.addLayout(radio3_layout)
        main_layout.addWidget(self.group3)

        # Calculation buttons
        button_layout = QHBoxLayout()
        operations = ["Add", "Subtract", "Dot Product", "Cross Product", "Plane Equation"]
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
        coord3 = self.get_coordinates(self.coord3_inputs) if operation == "Plane Equation" else None

        if coord1 is None or coord2 is None or (operation == "Plane Equation" and coord3 is None):
            self.result_display.setText("Error: Please enter valid numbers for coordinates.")
            return

        # Determine types
        type1 = "Vector" if self.vector1_radio.isChecked() else "Point"
        type2 = "Vector" if self.vector2_radio.isChecked() else "Point"
        type3 = "Vector" if self.vector3_radio.isChecked() else "Point" if operation == "Plane Equation" else None

        # Initialize result
        result_text = f"Operation: {operation}\n"
        result_text += f"Coordinate 1 ({type1}): {coord1}\n"
        result_text += f"Coordinate 2 ({type2}): {coord2}\n"
        if operation == "Plane Equation":
            result_text += f"Coordinate 3 ({type3}): {coord3}\n"

        # Perform calculations using VectorOperations
        try:
            if operation == "Add":
                result = VectorOperations.add(coord1, coord2, type1, type2)
                result_text += f"Result: {result}"
            elif operation == "Subtract":
                result = VectorOperations.subtract(coord1, coord2, type1, type2)
                result_text += f"Result: {result}"
            elif operation == "Dot Product":
                result = VectorOperations.dot_product(coord1, coord2, type1, type2)
                result_text += f"Result: {result}"
            elif operation == "Cross Product":
                result = VectorOperations.cross_product(coord1, coord2, type1, type2)
                result_text += f"Result: {result}"
            elif operation == "Plane Equation":
                a, b, c, d = VectorOperations.plane_equation(coord1, coord2, coord3, type1, type2, type3)
                result_text += f"Normalvektor: [{a} {b} {c}]\n"
                result_text += f"Plane Equation: {a}x + {b}y + {c}z = {d}\n"
                result_text += f"Plane Equation: {a}x + {b}y + {c}z -{d} = 0\n"
            else:
                result_text += "Error: Unknown operation."
        except Exception as e:
            result_text += f"Error: {str(e)}"

        self.result_display.setText(result_text)