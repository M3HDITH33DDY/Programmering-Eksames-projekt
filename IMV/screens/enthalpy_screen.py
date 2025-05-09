# Importerer nødvendige moduler og klasser fra PySide6 og standardbiblioteket
import json        # Til at læse og skrive JSON-data
import os          # Til fil- og stioperationer
import sys         # Til at detektere kørsel fra PyInstaller
import re          # Til at parse reaktionsstrenge med regulære udtryk

# PySide6 GUI-komponenter
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QLabel, QApplication
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize

class EditorButton(QPushButton):
    """
    En specialdesignet grøn knap med rundet udseende.
    Bruges til handlinger som 'Beregn' eller 'Tilføj'.
    """
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedSize(QSize(140, 45))  # Gør knappen fast i størrelse
        self.setStyleSheet("""
            QPushButton {
                border-radius: 15px;
                background-color: #15803D;
                color: #FFFFFF;
                padding: 12px;
                font-size: 16px;
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

class LineEdit(QLineEdit):
    """
    Et tilpasset inputfelt med mørk baggrund og hvid tekst.
    Bruges til at indtaste reaktioner og molekyler.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QLineEdit {
                background-color: #374151;
                color: #FFFFFF;
                border: 1px solid #4B5563;
                border-radius: 8px;
                padding: 8px;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }
        """)

class EnthalpyScreen(QWidget):
    """
    Hovedklasse for GUI-skærmen, hvor brugeren kan:
    - se molekyledata
    - tilføje nye molekyler
    - beregne ΔH° for reaktioner
    """
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #1E1E1E;")  # Sætter mørkt tema

        # Label til visning af fejl eller statusmeddelelser
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            font-size: 14px;
            font-family: Arial, sans-serif;
            color: #D1D5DB;
            padding: 5px;
        """)

        # Find sti til JSON-filen, afhængigt af om appen er pakket eller ej
        try:
            PATH = sys._MEIPASS  # Bruges når appen er pakket med PyInstaller
            self.json_file = os.path.join(PATH, "IMV", "screens", "enthalpy_data.json")
        except AttributeError:
            # Standard sti når man kører appen som Python-script
            PATH = os.path.dirname(os.path.abspath(__file__))
            self.json_file = os.path.join(PATH, "enthalpy_data.json")

        self.data = self.load_data()  # Indlæser eksisterende molekyledata fra JSON

        # Overordnet layout til hele vinduet
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)  # Marginer omkring layoutet
        layout.setSpacing(20)  # Lodret afstand mellem widgets

        # ---------- TABELSEKTION ----------

        # Container til tabel og dets overskrift
        table_container = QWidget()
        table_container.setStyleSheet("background-color: #2D2D2D; border-radius: 10px;")
        table_inner_layout = QVBoxLayout(table_container)
        table_inner_layout.setSpacing(10)
        table_inner_layout.setContentsMargins(10, 10, 10, 10)

        # Label over tabellen
        table_label = QLabel("Entalpi Data")
        table_label.setAlignment(Qt.AlignCenter)
        table_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            font-family: Arial, sans-serif;
            color: #FFFFFF;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #14532D, stop:1 #22C55E);
            border-radius: 10px;
            padding: 8px;
            letter-spacing: 1px;
        """)
        table_inner_layout.addWidget(table_label)

        # Selve tabellen, hvor molekyler og deres ΔHf°-værdier vises
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Molekyle", "ΔHf° (kJ/mol)"])
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #374151;
                color: #FFFFFF;
                border: 1px solid #4B5563;
                border-radius: 8px;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #374151;
                color: #FFFFFF;
                font-weight: bold;
                font-family: Arial, sans-serif;
                font-size: 14px;
                padding: 5px;
                border: none;
            }
        """)
        self.populate_table()  # Udfyld tabellen med eksisterende data
        table_inner_layout.addWidget(self.table)
        layout.addWidget(table_container)

        # ---------- INPUTSEKTION ----------

        # Container til inputfelter og knapper
        input_container = QWidget()
        input_container.setStyleSheet("background-color: #2D2D2D; border-radius: 10px;")
        input_inner_layout = QVBoxLayout(input_container)
        input_inner_layout.setSpacing(10)
        input_inner_layout.setContentsMargins(10, 10, 10, 10)

        # Label over inputområdet
        input_label = QLabel("Reaktion og Tilføjelse")
        input_label.setAlignment(Qt.AlignCenter)
        input_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            font-family: Arial, sans-serif;
            color: #FFFFFF;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #14532D, stop:1 #22C55E);
            border-radius: 10px;
            padding: 8px;
            letter-spacing: 1px;
        """)
        input_inner_layout.addWidget(input_label)

        # ----- Reaktionsinput og beregning -----
        reaction_layout = QHBoxLayout()
        self.reaction_input = LineEdit()
        self.reaction_input.setPlaceholderText("Indsæt reaktion (f.eks., 2H2 + O2 -> 2H2O)")
        reaction_layout.addWidget(self.reaction_input)

        # Knap til at beregne ΔH° for reaktionen
        calculate_button = EditorButton("Beregn ΔH°")
        calculate_button.clicked.connect(self.calculate_enthalpy)
        reaction_layout.addWidget(calculate_button)
        input_inner_layout.addLayout(reaction_layout)

        # Label til visning af resultatet
        self.result_label = QLabel("Indsæt reaktion for at beregne ΔH°")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("""
            font-size: 14px;
            font-family: Arial, sans-serif;
            color: #D1D5DB;
            padding: 5px;
        """)
        input_inner_layout.addWidget(self.result_label)

        # ----- Molekyleinput og tilføjelse -----
        add_layout = QHBoxLayout()

        # Input til nyt molekyles navn
        self.compound_input = LineEdit()
        self.compound_input.setPlaceholderText("Nyt molekyle (f.eks., CO2)")
        add_layout.addWidget(self.compound_input)

        # Input til ΔHf°-værdi
        self.delta_h_f_input = LineEdit()
        self.delta_h_f_input.setPlaceholderText("ΔHf° (kJ/mol)")
        add_layout.addWidget(self.delta_h_f_input)

        # Knap til at tilføje molekylet
        add_button = EditorButton("Tilføj Molekyle")
        add_button.clicked.connect(self.add_compound)
        add_layout.addWidget(add_button)
        input_inner_layout.addLayout(add_layout)

        input_inner_layout.addWidget(self.status_label)

        layout.addWidget(input_container)
        layout.addStretch()
        self.setLayout(layout)

    def get_writable_json_path(self):
        """Returnerer en sti til, hvor JSON-filen kan skrives sikkert (f.eks. i brugerens hjemmemappe)."""
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(os.path.expanduser("~"), "enthalpy_data.json")
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "enthalpy_data.json")

    def load_data(self):
        """Læser JSON-filen med molekyledata, hvis den findes. Returnerer en liste."""
        if os.path.exists(self.json_file):
            try:
                with open(self.json_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.status_label.setText(f"Fejl ved indlæsning: {str(e)}")
        else:
            self.status_label.setText(f"Fil ikke fundet: {self.json_file}")
        return []

    def save_data(self):
        """Gemmer molekyledata til JSON-filen."""
        self.json_file = self.get_writable_json_path()
        try:
            with open(self.json_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=4)
            self.status_label.setText("Data gemt.")
        except Exception as e:
            self.status_label.setText(f"Fejl ved gemning: {str(e)}")

    def populate_table(self):
        """Opdaterer tabellen med alle molekyler fra data."""
        self.table.setRowCount(len(self.data))
        for row, item in enumerate(self.data):
            self.table.setItem(row, 0, QTableWidgetItem(item.get("compound", "")))
            self.table.setItem(row, 1, QTableWidgetItem(str(item.get("delta_h_f", 0.0))))
        self.table.resizeColumnsToContents()

    def add_compound(self):
        """Tilføjer et nyt molekyle fra inputfelterne til data og opdaterer tabellen."""
        try:
            compound = self.compound_input.text().strip()
            delta_h_f = float(self.delta_h_f_input.text().strip())

            if not compound:
                raise ValueError("Molekyle mangler")

            for item in self.data:
                if item["compound"].lower() == compound.lower():
                    raise ValueError("Molekyle findes allerede")

            self.data.append({"compound": compound, "delta_h_f": delta_h_f})
            self.save_data()
            self.populate_table()
            self.compound_input.clear()
            self.delta_h_f_input.clear()
        except ValueError as e:
            self.status_label.setText(f"Fejl: {str(e)}")

    def parse_reaction(self, reaction):
        """Parser en reaktionsstreng til lister med reaktanter og produkter."""
        try:
            sides = reaction.replace(' ', '').split('->')
            if len(sides) != 2:
                raise ValueError("Brug '->' i reaktionen")

            def parse_side(side):
                result = []
                for term in side.split('+'):
                    if not term:
                        continue
                    match = re.match(r'^(\d*)([A-Za-z][A-Za-z0-9]*)', term)
                    if not match:
                        raise ValueError(f"Ugyldigt input: {term}")
                    coeff_str, compound = match.groups()
                    coeff = int(coeff_str) if coeff_str else 1
                    result.append({"compound": compound, "coefficient": coeff})
                return result

            reactants = parse_side(sides[0])
            products = parse_side(sides[1])
            return reactants, products
        except Exception as e:
            raise ValueError(f"Fejl i parsing: {str(e)}")

    def calculate_enthalpy(self):
        """Beregner ΔH° for en given kemisk reaktion ved at bruge databasen."""
        try:
            reaction = self.reaction_input.text().strip()
            if not reaction:
                raise ValueError("Indtast en reaktion")

            reactants, products = self.parse_reaction(reaction)

            # Summér ΔHf° for produkter
            sum_products = 0.0
            for item in products:
                for data_item in self.data:
                    if data_item["compound"].lower() == item["compound"].lower():
                        sum_products += item["coefficient"] * data_item["delta_h_f"]
                        break
                else:
                    raise ValueError(f"'{item['compound']}' ikke fundet i databasen")

            # Summér ΔHf° for reaktanter
            sum_reactants = 0.0
            for item in reactants:
                for data_item in self.data:
                    if data_item["compound"].lower() == item["compound"].lower():
                        sum_reactants += item["coefficient"] * data_item["delta_h_f"]
                        break
                else:
                    raise ValueError(f"'{item['compound']}' ikke fundet i databasen")

            # ΔH° = produkter - reaktanter
            delta_h = sum_products - sum_reactants
            self.result_label.setText(f"ΔH° = {delta_h:.2f} kJ/mol")
        except ValueError as e:
            self.result_label.setText(f"Fejl: {str(e)}")
        except Exception as e:
            self.result_label.setText(f"Fejl ved beregning af ΔH°: {str(e)}")