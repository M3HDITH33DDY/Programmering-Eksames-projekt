import numpy as np
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton,
    QRadioButton, QTextEdit, QGroupBox
)
from PySide6.QtCore import Qt
from vector_calculations import VectorOperations

class CoordinateInput(QWidget):
    """A reusable widget for coordinate input with vector/point selection."""
    def __init__(self, title):
        super().__init__()
        self.group = QGroupBox(title)
        layout = QVBoxLayout()
        self.group.setLayout(layout)

        # Coordinate input fields
        self.inputs = []
        coord_layout = QHBoxLayout()
        for label in ['X:', 'Y:', 'Z:']:
            lbl = QLabel(label)
            input_field = QLineEdit()
            input_field.setPlaceholderText("0.0")
            coord_layout.addWidget(lbl)
            coord_layout.addWidget(input_field)
            self.inputs.append(input_field)
        layout.addLayout(coord_layout)

        # Radio buttons for vector/point
        self.vector_radio = QRadioButton("Vector")
        self.point_radio = QRadioButton("Point")
        self.vector_radio.setChecked(True)
        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.vector_radio)
        radio_layout.addWidget(self.point_radio)
        layout.addLayout(radio_layout)

    def get_widget(self):
        """Return the QGroupBox widget for adding to a layout."""
        return self.group

    def get_coordinates(self):
        """Retrieve coordinates as a numpy array or None if invalid."""
        try:
            coords = [float(inp.text()) if inp.text().strip() else 0.0 for inp in self.inputs]
            return np.array(coords)
        except ValueError:
            return None

    def get_type(self):
        """Return the selected type ('Vector' or 'Point')."""
        return "Vector" if self.vector_radio.isChecked() else "Point"

class VectorCalculator(QWidget):
    def __init__(self):
        super().__init__()

        # Main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Create coordinate input groups
        self.coord_inputs = [
            CoordinateInput("Coordinate 1"),
            CoordinateInput("Coordinate 2"),
            CoordinateInput("Coordinate 3")
        ]
        for coord_input in self.coord_inputs:
            main_layout.addWidget(coord_input.get_widget())

        # Calculation buttons
        button_layout = QHBoxLayout()
        operations = ["Addition", "Subtraktion", "Skalar Produkt", "Kryds Produkt", "Planens Ligning", "Alt"]
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

    def calculate(self, operation):
        # Get coordinates and types
        coord1 = self.coord_inputs[0].get_coordinates()
        coord2 = self.coord_inputs[1].get_coordinates()
        coord3 = self.coord_inputs[2].get_coordinates() if operation in ("Plane Equation", "Alt") else None

        if coord1 is None or coord2 is None or (operation in ("Plane Equation", "Alt") and coord3 is None):
            self.result_display.setText("Error: Please enter valid numbers for coordinates.")
            return

        # Get types
        type1 = self.coord_inputs[0].get_type()
        type2 = self.coord_inputs[1].get_type()
        type3 = self.coord_inputs[2].get_type() if operation in ("Plane Equation", "Alt") else None

        # Initialize result
        result_text = f"Operation: {operation}\n"
        result_text += f"Coordinate 1 ({type1}): {coord1}\n"
        result_text += f"Coordinate 2 ({type2}): {coord2}\n"
        if operation in ("Plane Equation", "Alt"):
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
                result_text += f"Plane Equation: {a}x + {b}y + {c}z {-d} = 0\n"
            elif operation == "Alt":
                result = VectorOperations.add(coord1, coord2, type1, type2)
                result_text += f"Addering af vektor 1 og 2: {result}\n"
                result = VectorOperations.subtract(coord1, coord2, type1, type2)
                result_text += f"Substraktion af vektor 1 og 2: {result}\n"
                result = VectorOperations.dot_product(coord1, coord2, type1, type2)
                result_text += f"Prikprodukt af vektor 1 og 2: {result}\n"
                result = VectorOperations.cross_product(coord1, coord2, type1, type2)
                result_text += f"Noamlvektor af vektor 1 og 2: {result}\n"
                a, b, c, d = VectorOperations.plane_equation(coord1, coord2, coord3, type1, type2, type3)
                result_text += f"Normalvektor: [{a} {b} {c}]\n"
                result_text += f"Plane Equation: {a}x + {b}y + {c}z = {d}\n"
                result_text += f"Plane Equation: {a}x + {b}y + {c}z {-d} = 0\n"
            else:
                result_text += "Error: Unknown operation."
        except Exception as e:
            result_text += f"Error: {str(e)}"

        self.result_display.setText(result_text)