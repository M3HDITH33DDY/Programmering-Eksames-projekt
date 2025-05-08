# screens/rekus_screen.py

import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel,
    QPushButton, QTextEdit, QMessageBox
)
from PySide6.QtGui import QFont
from IMV.screens.reccurence_calculations import RecurrenceSolver, format_polynomial

class RecurrenceGUI(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("a(n) = 4*a(n-1) - 4*a(n-2)")
        layout.addWidget(QLabel("Rekursionsligning:"))
        layout.addWidget(self.input_line)

        self.initial_values = QTextEdit()
        self.initial_values.setPlaceholderText("a(0)=1\na(1)=2")
        layout.addWidget(QLabel("Startværdier:"))
        layout.addWidget(self.initial_values)

        self.solve_button = QPushButton("Løs")
        self.solve_button.clicked.connect(self.solve)
        layout.addWidget(self.solve_button)

        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        self.result_area.setFont(QFont("Courier", 11))
        layout.addWidget(QLabel("Resultat:"))
        layout.addWidget(self.result_area)

    def solve(self):
        # Hent brugerens indtastede rekursive ligning og startværdier
        equation = self.input_line.text()
        init_vals = self.initial_values.toPlainText().strip()
        
        try:
            # Opret en instans af løseren med ligningen og startværdierne
            solver = RecurrenceSolver(equation, init_vals)

            if init_vals:  # Hvis brugeren har angivet startværdier
                # Beregn koefficienter, rødder, generel løsning og fuld løsning
                coeffs, roots, general, full = solver.solve()
            else:  # Kun generel løsning uden konstanter
                coeffs, roots, general = solver.solve_general_only()
                full = "Ingen startværdier angivet – konstanter ikke bestemt."

            # Formater rødderne, afrund reelle rødder og vis komplekse som tekst
            root_lines = ", ".join([
                f"{r.real:.3f}" if abs(r.imag) < 1e-10 else str(r)
                for r in roots
            ])

            # Sammensæt resultattekst til visning
            result = (
                f"Karakteristisk ligning:\n{format_polynomial(coeffs)} = 0\n\n"
                f"Rødder: {root_lines}\n\n"
                f"Generel løsning:\na(n) = {general}\n\n"
                f"{'Løsning med startværdier:\na(n) = ' + full if init_vals else full}"
            )

            # Vis resultatet i brugergrænsefladens tekstfelt
            self.result_area.setText(result)

        except Exception as e:
            # Vis en fejlmeddelelse hvis der opstår en undtagelse
            QMessageBox.critical(self, "Fejl", str(e))
