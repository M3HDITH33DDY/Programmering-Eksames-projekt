from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton, QTextEdit, QGroupBox
from PySide6.QtCore import Qt
from screens.triangle_calculations import TriangleCalculations

class TriangleCalculator(QWidget):
    """Skærm til beregning af trekants egenskaber baseret på sider og/eller vinkler."""

    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #1E1E1E; color: #FFFFFF;")
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Title
        title = QLabel("Trekantsberegner")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            font-family: Arial, sans-serif;
            color: #D1D5DB;
            padding: 8px;
        """)
        main_layout.addWidget(title)

        # Sides input (a, b, c)
        self.sides_group = QGroupBox("Sider")
        sides_layout = QVBoxLayout()
        self.sides_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                color: #D1D5DB;
                border: 1px solid #4B5563;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 3px;
                color: #D1D5DB;
            }
        """)
        self.sides_group.setLayout(sides_layout)

        self.side_inputs = []
        side_input_layout = QHBoxLayout()
        for label in ['a:', 'b:', 'c:']:
            lbl = QLabel(label)
            input_field = QLineEdit()
            input_field.setPlaceholderText("0.0")
            input_field.setStyleSheet("""
                background-color: #2D2D2D;
                color: #FFFFFF;
                border: 1px solid #4B5563;
                border-radius: 5px;
                padding: 5px;
                font-family: Arial, sans-serif;
            """)
            side_input_layout.addWidget(lbl)
            side_input_layout.addWidget(input_field)
            self.side_inputs.append(input_field)
        sides_layout.addLayout(side_input_layout)
        main_layout.addWidget(self.sides_group)

        # Angles input (A, B, C)
        self.angles_group = QGroupBox("Vinkler (grader)")
        angles_layout = QVBoxLayout()
        self.angles_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                color: #D1D5DB;
                border: 1px solid #4B5563;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 3px;
                color: #D1D5DB;
            }
        """)
        self.angles_group.setLayout(angles_layout)

        self.angle_inputs = []
        angle_input_layout = QHBoxLayout()
        for label in ['A:', 'B:', 'C:']:
            lbl = QLabel(label)
            input_field = QLineEdit()
            input_field.setPlaceholderText("0.0")
            input_field.setStyleSheet("""
                background-color: #2D2D2D;
                color: #FFFFFF;
                border: 1px solid #4B5563;
                border-radius: 5px;
                padding: 5px;
                font-family: Arial, sans-serif;
            """)
            angle_input_layout.addWidget(lbl)
            angle_input_layout.addWidget(input_field)
            self.angle_inputs.append(input_field)
        angles_layout.addLayout(angle_input_layout)
        main_layout.addWidget(self.angles_group)

        # Calculation buttons
        button_layout = QHBoxLayout()
        operations = ["Beregn", "Ryd"]
        self.buttons = {}
        for op in operations:
            btn = QPushButton(op)
            btn.setStyleSheet("""
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
            btn.clicked.connect(lambda checked, operation=op: self.handle_button(operation))
            button_layout.addWidget(btn)
            self.buttons[op] = btn
        main_layout.addLayout(button_layout)

        # Result display
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setPlaceholderText("Beregningsresultater vises her...")
        self.result_display.setStyleSheet("""
            background-color: #2D2D2D;
            color: #FFFFFF;
            border: 1px solid #4B5563;
            border-radius: 5px;
            padding: 5px;
            font-family: Arial, sans-serif;
        """)
        main_layout.addWidget(self.result_display)

    def get_inputs(self, inputs):
        """Hent værdier fra inputfelter og konverter til float."""
        try:
            return [float(inp.text()) if inp.text().strip() else 0.0 for inp in inputs]
        except ValueError:
            return None

    def handle_button(self, operation):
        """Håndter knaptryk (Beregn eller Ryd)."""
        if operation == "Ryd":
            for inp in self.side_inputs + self.angle_inputs:
                inp.clear()
            self.result_display.clear()
            return

        # Hent input
        sides = self.get_inputs(self.side_inputs)
        angles = self.get_inputs(self.angle_inputs)

        try:
            # Prioriter sider, hvis de er angivet og gyldige
            if sides is not None and all(s > 0 for s in sides):
                result = TriangleCalculations.calculate_from_sides(*sides, angles=angles if angles is not None and any(a > 0 for a in angles) else None)
                self.display_results(result, "Beregning ud fra sider")
            # Fallback til vinkler og én side, hvis sider mangler eller er ugyldige
            elif angles is not None and all(a > 0 for a in angles) and sides is not None and sides[0] > 0:
                result = TriangleCalculations.calculate_from_side_angles(sides[0], *angles)
                self.display_results(result, "Beregning ud fra vinkler og side a")
            else:
                self.result_display.setText("Fejl: Indtast gyldige positive tal for alle sider eller én side og alle vinkler.")
        except Exception as e:
            self.result_display.setText(f"Fejl: {str(e)}")

    def display_results(self, result, calculation_type):
        """Vis beregningsresultater i result_display."""
        result_text = f"{calculation_type}\n"
        result_text += f"Sider:\n"
        result_text += f"a: {result['sides']['a']:.2f}\n"
        result_text += f"b: {result['sides']['b']:.2f}\n"
        result_text += f"c: {result['sides']['c']:.2f}\n"
        result_text += f"Vinkler:\n"
        result_text += f"A: {result['angles']['A']:.2f}°\n"
        result_text += f"B: {result['angles']['B']:.2f}°\n"
        result_text += f"C: {result['angles']['C']:.2f}°\n"
        result_text += f"Omkreds: {result['perimeter']:.2f}\n"
        result_text += f"Areal: {result['area']:.2f}"
        self.result_display.setText(result_text)