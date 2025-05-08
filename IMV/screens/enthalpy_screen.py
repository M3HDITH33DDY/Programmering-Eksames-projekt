import json
import os
import sys
import re
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QLabel, QApplication
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize

class EditorButton(QPushButton):
    """En knap med design inspireret af HomeScreen's DraggableButton, uden drag-and-drop."""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedSize(QSize(140, 45))
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
    """En skærm til at beregne molar standard entalpi og administrere molekyledata i en mørk-tema brugergrænseflade."""

    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #1E1E1E;")

        # Initialize status_label early
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            font-size: 14px;
            font-family: Arial, sans-serif;
            color: #D1D5DB;
            padding: 5px;
        """)

        # Loader JSON file
        try:
            PATH = sys._MEIPASS  # PyInstaller
            self.json_file = os.path.join(PATH, "IMV", "screens", "enthalpy_data.json")
        except AttributeError:
            PATH = os.path.dirname(os.path.abspath(__file__))
            self.json_file = os.path.join(PATH, "enthalpy_data.json")
        
        
        self.data = self.load_data()

        # Main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Table container
        table_container = QWidget()
        table_container.setStyleSheet("background-color: #2D2D2D; border-radius: 10px;")
        table_inner_layout = QVBoxLayout(table_container)
        table_inner_layout.setSpacing(10)
        table_inner_layout.setContentsMargins(10, 10, 10, 10)

        # Gradient title for table
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

        # Table for molecule and ΔH_f° values
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
        self.populate_table()
        table_inner_layout.addWidget(self.table)

        layout.addWidget(table_container)

        # Input, buttons, and status container
        input_container = QWidget()
        input_container.setStyleSheet("background-color: #2D2D2D; border-radius: 10px;")
        input_inner_layout = QVBoxLayout(input_container)
        input_inner_layout.setSpacing(10)
        input_inner_layout.setContentsMargins(10, 10, 10, 10)

        # Gradient title for input section
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

        # Reaction input and button
        reaction_layout = QHBoxLayout()
        self.reaction_input = LineEdit()
        self.reaction_input.setPlaceholderText("Indsæt reaktion (f.eks., 2H2 + O2 -> 2H2O)")
        reaction_layout.addWidget(self.reaction_input)

        calculate_button = EditorButton("Beregn ΔH°")
        calculate_button.clicked.connect(self.calculate_enthalpy)
        reaction_layout.addWidget(calculate_button)
        input_inner_layout.addLayout(reaction_layout)

        # Result label
        self.result_label = QLabel("Indsæt reaktion for at beregne ΔH°")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("""
            font-size: 14px;
            font-family: Arial, sans-serif;
            color: #D1D5DB;
            padding: 5px;
        """)
        input_inner_layout.addWidget(self.result_label)

        # Add compound input and button
        add_layout = QHBoxLayout()
        self.compound_input = LineEdit()
        self.compound_input.setPlaceholderText("Nyt molekyle (f.eks., CO2)")
        add_layout.addWidget(self.compound_input)

        self.delta_h_f_input = LineEdit()
        self.delta_h_f_input.setPlaceholderText("ΔHf° (kJ/mol)")
        add_layout.addWidget(self.delta_h_f_input)

        add_button = EditorButton("Tilføj Molekyle")
        add_button.clicked.connect(self.add_compound)
        add_layout.addWidget(add_button)
        input_inner_layout.addLayout(add_layout)

        # Status label (already defined earlier)
        input_inner_layout.addWidget(self.status_label)

        layout.addWidget(input_container)
        layout.addStretch()

        self.setLayout(layout)

    def get_writable_json_path(self):
        """Get a writable path for saving the JSON file."""
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(os.path.expanduser("~"), "enthalpy_data.json")
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "enthalpy_data.json")

    def load_data(self):
        """Indlæser data fra JSON-fil."""
        if os.path.exists(self.json_file):
            try:
                with open(self.json_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.status_label.setText(f"Fejl ved indlæsning af '{os.path.basename(self.json_file)}': {str(e)}")
                return []
        self.status_label.setText(f"JSON-fil ikke fundet: {self.json_file}")
        return []

    def save_data(self):
        """Gemmer data til JSON-fil."""
        self.json_file = self.get_writable_json_path()
        print(f"Saving JSON to: {self.json_file}")  # Debug
        try:
            with open(self.json_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=4)
            self.status_label.setText(f"Molekylet er gemt til '{os.path.basename(self.json_file)}'")
        except Exception as e:
            self.status_label.setText(f"Fejl ved gemning af '{os.path.basename(self.json_file)}': {str(e)}")

    # Rest of the class (populate_table, add_compound, parse_reaction, calculate_enthalpy) remains unchanged

    def populate_table(self):
        """Udfylder tabellen med data fra JSON."""
        self.table.setRowCount(len(self.data))
        for row, item in enumerate(self.data):
            self.table.setItem(row, 0, QTableWidgetItem(item.get("compound", "")))
            self.table.setItem(row, 1, QTableWidgetItem(str(item.get("delta_h_f", 0.0))))
        self.table.resizeColumnsToContents()

    def add_compound(self):
        """Tilføjer et nyt molekyle til data og opdaterer tabellen."""
        try:
            compound = self.compound_input.text().strip()
            delta_h_f = float(self.delta_h_f_input.text().strip())
            
            if not compound:
                raise ValueError("Molekyle kan ikke være tomt")
            
            for item in self.data:
                if item["compound"].lower() == compound.lower():
                    raise ValueError(f"Molekyle '{compound}' findes allerede")
            
            new_item = {
                "compound": compound,
                "delta_h_f": delta_h_f
            }
            
            self.data.append(new_item)
            self.save_data()
            self.populate_table()
            
            self.compound_input.clear()
            self.delta_h_f_input.clear()
            
        except ValueError as e:
            self.status_label.setText(f"Fejl: {str(e)}")
        except Exception as e:
            self.status_label.setText(f"Fejl ved tilføjelse af molekyle: {str(e)}")

    def parse_reaction(self, reaction):
        """Parser en reaktionsstreng til reaktanter og produkter med koefficienter."""
        try:
            sides = reaction.replace(' ', '').split('->')
            if len(sides) != 2:
                raise ValueError("Reaktionen skal indeholde '->' for at separere reaktanter og produkter")
            
            reactants_str, products_str = sides
            
            def parse_side(side):
                """Parser en side af reaktionen til forbindelser og koefficienter."""
                result = []
                terms = side.split('+')
                for term in terms:
                    if not term:
                        continue
                    match = re.match(r'^(\d*)([A-Za-z][A-Za-z0-9]*)', term)
                    if not match:
                        raise ValueError(f"Ugyldig term: {term}")
                    coeff_str, compound = match.groups()
                    coeff = int(coeff_str) if coeff_str else 1
                    result.append({"compound": compound, "coefficient": coeff})
                return result
            
            reactants = parse_side(reactants_str)
            products = parse_side(products_str)
            
            return reactants, products
        except Exception as e:
            raise ValueError(f"Fejl ved parsing af reaktion: {str(e)}")

    def calculate_enthalpy(self):
        """Beregner ændringen i molar standard entalpi for reaktionen."""
        try:
            reaction = self.reaction_input.text().strip()
            if not reaction:
                raise ValueError("Reaktion må ikke være tom!")
            
            reactants, products = self.parse_reaction(reaction)
            
            sum_products = 0.0
            sum_reactants = 0.0
            
            for item in products:
                compound = item["compound"]
                coeff = item["coefficient"]
                found = False
                for data_item in self.data:
                    if data_item["compound"].lower() == compound.lower():
                        sum_products += coeff * data_item["delta_h_f"]
                        found = True
                        break
                if not found:
                    raise ValueError(f"Forbindelse '{compound}' findes ikke i databasen!")
            
            for item in reactants:
                compound = item["compound"]
                coeff = item["coefficient"]
                found = False
                for data_item in self.data:
                    if data_item["compound"].lower() == compound.lower():
                        sum_reactants += coeff * data_item["delta_h_f"]
                        found = True
                        break
                if not found:
                    raise ValueError(f"Forbindelse '{compound}' findes ikke i databasen!")
            
            delta_h = sum_products - sum_reactants
            self.result_label.setText(f"ΔH° = {delta_h:.2f} kJ/mol")
            
        except ValueError as e:
            self.result_label.setText(f"Fejl: {str(e)}")
        except Exception as e:
            self.result_label.setText(f"Fejl ved beregning af ΔH°: {str(e)}")