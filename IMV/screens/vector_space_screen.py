import numpy as np
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton,
    QRadioButton, QTextEdit, QGroupBox
)
from PySide6.QtCore import Qt
from IMV.screens.vector_calculations import VectorOperations

class CoordinateInput(QWidget):
    def __init__(self, title):
        super().__init__()
        self.group = QGroupBox(title)
        layout = QVBoxLayout()
        self.group.setLayout(layout)

        # Input felter til x, y, z
        self.inputs = []
        coord_layout = QVBoxLayout()
        for label in ['X:', 'Y:', 'Z:']:
            lbl = QLabel(label)
            input_field = QLineEdit()
            input_field.setPlaceholderText("0.0")
            coord_layout.addWidget(lbl)
            coord_layout.addWidget(input_field)
            self.inputs.append(input_field)
        layout.addLayout(coord_layout)

        # Radio knapper: Vektor eller Punkt
        self.vector_radio = QRadioButton("Vektor")
        self.point_radio = QRadioButton("Punkt")
        self.vector_radio.setChecked(True)
        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.vector_radio)
        radio_layout.addWidget(self.point_radio)
        layout.addLayout(radio_layout)

    def get_widget(self):
        return self.group

    def get_coordinates(self):
        """Returnerer koordinater eller (0,0,0) hvis fejl"""
        try:
            coords = [float(inp.text()) if inp.text().strip() else 0.0 for inp in self.inputs]
            return np.array(coords)
        except ValueError:
            return np.array([0.0, 0.0, 0.0])

    def get_type(self):
        return "Vektor" if self.vector_radio.isChecked() else "Punkt"


class VectorCalculator(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Koordinatfelter i en vandret række
        coords_layout = QHBoxLayout()
        self.coord_inputs = [
            CoordinateInput("1. Koordinat"),
            CoordinateInput("2. Koordinat"),
            CoordinateInput("3. Koordinat")
        ]
        for coord_input in self.coord_inputs:
            coords_layout.addWidget(coord_input.get_widget())
        main_layout.addLayout(coords_layout)

        # Beregningsknapper
        button_layout = QHBoxLayout()
        operations = ["Addition", "Subtraktion", "Skalar Produkt", "Kryds Produkt", "Planens Ligning", "Alt"]
        self.buttons = {}
        for op in operations:
            btn = QPushButton(op)
            btn.clicked.connect(lambda checked, operation=op: self.calculate(operation))
            button_layout.addWidget(btn)
            self.buttons[op] = btn
        main_layout.addLayout(button_layout)

        # Resultatvisning
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setPlaceholderText("Beregninger vises her")
        main_layout.addWidget(self.result_display)

    def calculate(self, operation):
        coord1 = self.coord_inputs[0].get_coordinates()
        coord2 = self.coord_inputs[1].get_coordinates()
        coord3 = None
        if operation in ("Planens Ligning", "Alt"):
            coord3 = self.coord_inputs[2].get_coordinates()

        type1 = self.coord_inputs[0].get_type()
        type2 = self.coord_inputs[1].get_type()
        type3 = self.coord_inputs[2].get_type() if operation in ("Planens Ligning", "Alt") else None

        result_text = f"Handling: {operation}\n"
        result_text += f"1. Koordinat ({type1}): {coord1}\n"
        result_text += f"2. Koordinat ({type2}): {coord2}\n"
        if operation in ("Planens Ligning", "Alt"):
            result_text += f"3. Koordinat ({type3}): {coord3}\n"

        try:
            if operation == "Addition":
                result = VectorOperations.add(coord1, coord2, type1, type2)
                result_text += f"Resultat: {result}"
            elif operation == "Subtraktion":
                result = VectorOperations.subtract(coord1, coord2, type1, type2)
                result_text += f"Resultat: {result}"
            elif operation == "Skalar Produkt":
                result = VectorOperations.dot_product(coord1, coord2, type1, type2)
                result_text += f"Resultat: {result}"
            elif operation == "Kryds Produkt":
                result = VectorOperations.cross_product(coord1, coord2, type1, type2)
                result_text += f"Normalvektor: {result}"
            elif operation == "Planens Ligning":
                a, b, c, d = VectorOperations.plane_equation(coord1, coord2, coord3, type1, type2, type3)
                result_text += f"Normalvektor: [{a} {b} {c}]\n"
                result_text += f"Planens Ligning: {a}x + {b}y + {c}z = {d}\n"
                result_text += f"Omskrevet: {a}x + {b}y + {c}z - {d} = 0"
            elif operation == "Alt":
                result = VectorOperations.add(coord1, coord2, type1, type2)
                result_text += f"Addition: {result}\n"
                result = VectorOperations.subtract(coord1, coord2, type1, type2)
                result_text += f"Subtraktion: {result}\n"
                result = VectorOperations.dot_product(coord1, coord2, type1, type2)
                result_text += f"Skalarprodukt: {result}\n"
                result = VectorOperations.cross_product(coord1, coord2, type1, type2)
                result_text += f"Normalvektor: {result}\n"
                a, b, c, d = VectorOperations.plane_equation(coord1, coord2, coord3, type1, type2, type3)
                result_text += f"Planens Ligning: {a}x + {b}y + {c}z = {d}\n"
                result_text += f"Omskrevet: {a}x + {b}y + {c}z - {d} = 0"
            else:
                result_text += "Fejl: Ukendt handling."
        except Exception as e:
            result_text += f"\nFejl: {str(e)}"

        self.result_display.setText(result_text)

