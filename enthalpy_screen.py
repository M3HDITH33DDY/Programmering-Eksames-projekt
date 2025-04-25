import json
import os
import re
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QHBoxLayout
from PySide6.QtCore import Qt

class EnthalpyScreen(QWidget):
    def __init__(self):
        super().__init__()
        #Henvisning til navendte JSON-fil
        self.json_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "enthalpy_data.json")
        self.data = self.load_data()
        
        # Main layout
        layout = QVBoxLayout()
        
        # Titel indenpå siden i centrum
        title = QLabel("Molar Standard Entalpi Beregner")
        title.setAlignment(Qt.AlignCenter) #Alligner tekst til centrum
        layout.addWidget(title)
        
        # Tabel til visning af molekyle samt ΔH-værdi
        self.table = QTableWidget()
        self.table.setColumnCount(2) #2 kolonner
        self.table.setHorizontalHeaderLabels(["Molekyle", "ΔHf° (kJ/mol)"])
        self.populate_table()
        layout.addWidget(self.table)
        
        # Input for reaktion
        reaction_layout = QHBoxLayout()
        self.reaction_input = QLineEdit()
        self.reaction_input.setPlaceholderText("Indsæt reaktion (f.eks., 2H2 + O2 -> 2H2O)") #Pladsholder, indtil bruger skriver
        reaction_layout.addWidget(self.reaction_input)
        #Knap
        calculate_button = QPushButton("Beregn ΔH°")
        calculate_button.clicked.connect(self.calculate_enthalpy)
        reaction_layout.addWidget(calculate_button)
        layout.addLayout(reaction_layout)
        
        # Resultat
        self.result_label = QLabel("Indsæt reaktion for at beregne ΔH°") #pladsholder
        self.result_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.result_label)
        
        # Input område for navnet af nyt molekyle
        add_layout = QHBoxLayout()
        self.compound_input = QLineEdit()
        self.compound_input.setPlaceholderText("Nyt molekyle (f.eks., CO2)")
        add_layout.addWidget(self.compound_input)
        #Input for data for det nye molekyle
        self.delta_h_f_input = QLineEdit()
        self.delta_h_f_input.setPlaceholderText("ΔHf° (kJ/mol)")
        add_layout.addWidget(self.delta_h_f_input)
        
        add_button = QPushButton("Tilføj Molekyle")
        add_button.clicked.connect(self.add_compound)
        add_layout.addWidget(add_button)
        layout.addLayout(add_layout)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def load_data(self):
        """Load data from JSON file."""
        if os.path.exists(self.json_file):
            try:
                with open(self.json_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self.status_label.setText(f"Fejl ved indlæsning: {str(e)}")
                return []
        return []
    
    def save_data(self):
        """Save data to JSON file."""
        try:
            with open(self.json_file, 'w') as f:
                json.dump(self.data, f, indent=4)
            self.status_label.setText("Molekylet er gemt")
        except Exception as e:
            self.status_label.setText(f"Fejl ved gemning af molekyle: {str(e)}")
    
    def populate_table(self):
        """Populate the table with data from JSON."""
        self.table.setRowCount(len(self.data))
        for row, item in enumerate(self.data):
            self.table.setItem(row, 0, QTableWidgetItem(item.get("compound", "")))
            self.table.setItem(row, 1, QTableWidgetItem(str(item.get("delta_h_f", 0.0))))
        self.table.resizeColumnsToContents()
    
    def add_compound(self):
        """Add a new compound to the data and update the table."""
        try:
            compound = self.compound_input.text().strip()
            delta_h_f = float(self.delta_h_f_input.text().strip())
            
            if not compound:
                raise ValueError("Molekyle kan ikke være tomt")
            
            # Check for duplicate compounds
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
            
            # Clear input fields
            self.compound_input.clear()
            self.delta_h_f_input.clear()
            
        except ValueError as e:
            self.status_label.setText(f"Fejl: {str(e)}")
        except Exception as e:
            self.status_label.setText(f"Fejl ved tilføjelse af Molekyle: {str(e)}")
    
    def parse_reaction(self, reaction):
        """Parse a reaction string into reactants and products with coefficients."""
        try:
            # Split into reactants and products
            sides = reaction.replace(' ', '').split('->')
            if len(sides) != 2:
                raise ValueError("Reaktionen skal indeholde '->' for separaring af reaktanter og produkter")
            
            reactants_str, products_str = sides
            
            def parse_side(side):
                """Parse one side of the reaction into compounds and coefficients."""
                result = []
                # Split by '+' and handle coefficients
                terms = side.split('+')
                for term in terms:
                    if not term:
                        continue
                    # Match coefficient (optional) and compound
                    match = re.match(r'^(\d*)([A-Za-z][A-Za-z0-9]*)', term)
                    if not match:
                        raise ValueError(f"Invalid term: {term}")
                    coeff_str, compound = match.groups()
                    coeff = int(coeff_str) if coeff_str else 1
                    result.append({"compound": compound, "coefficient": coeff})
                return result
            
            reactants = parse_side(reactants_str)
            products = parse_side(products_str)
            
            return reactants, products
        except Exception as e:
            raise ValueError(f"Error parsing reaction: {str(e)}")
    
    def calculate_enthalpy(self):
        """Calculate the molar standard enthalpy change for the reaction."""
        try:
            reaction = self.reaction_input.text().strip()
            if not reaction:
                raise ValueError("Reaction cannot be empty!")
            
            # Parse reaction
            reactants, products = self.parse_reaction(reaction)
            
            # Calculate ΔH° = Σ n_p ΔH_f°(products) - Σ n_r ΔH_f°(reactants)
            sum_products = 0.0
            sum_reactants = 0.0
            
            # Lookup ΔH_f° for each compound
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
                    raise ValueError(f"Compound '{compound}' not found in database!")
            
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
                    raise ValueError(f"Compound '{compound}' not found in database!")
            
            delta_h = sum_products - sum_reactants
            self.result_label.setText(f"ΔH° = {delta_h:.2f} kJ/mol")
            
        except ValueError as e:
            self.result_label.setText(f"Error: {str(e)}")
        except Exception as e:
            self.result_label.setText(f"Error calculating ΔH°: {str(e)}")