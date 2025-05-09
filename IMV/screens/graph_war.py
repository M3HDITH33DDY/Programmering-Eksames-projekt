import math
import random
import numpy as np
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtGui import QPainter, QPen
from PySide6.QtCore import Qt, QPoint


class Enemy:
    def __init__(self, width, height):
        
        self._state = True  # Levende
        self._size = 10  # Diameter
        self._x = random.randint(width - 85, width - 55) #Start x-pos
        self._y = random.randint(50, height - 150) #Start y-pos

        # Gem relativ position mellem skærm (Anvendes til ændring af størrelse af vinduet)
        self._x_ratio = self._x / width
        self._y_ratio = self._y / height

    # ---- Properties ----
    #Getter for state
    @property 
    def state(self):
        return self._state 
    #setter for state
    @state.setter
    def state(self, value):
        if not isinstance(value, bool):
            raise ValueError("state skal være True eller False")
        self._state = value
    #Getter for size
    @property
    def size(self):
        return self._size
    #Getter for x-pos
    @property
    def x(self):
        return self._x
    #Getter for y-pos
    @property
    def y(self):
        return self._y
    #Opdatering af position, når vinduets størrelse ændres
    def update_position(self, new_width, new_height):
        self._x = int(self._x_ratio * new_width)
        self._y = int(self._y_ratio * new_height)

    



class GraphWarScreen(QWidget):
    def __init__(self):
        super().__init__()
        
        # Layout
        self.layout = QVBoxLayout()
        self.layout.addStretch() #Mellemrum, rykker objekter ned i bunden
        self.title = QLabel("Graf Krig")
        self.scale_text = QLabel("Skalering af banen        ")
        self.title.setAlignment(Qt.AlignCenter)
        self.scale_text.setAlignment(Qt.AlignRight)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.scale_text)

        input_layout = QHBoxLayout()
        self.function_input = QLineEdit("x**2 / 100") #Start (Eksempel)
        self.scale_input = QLineEdit("0.01") #Start skalering
        self.scale_input.setFixedWidth(120)
        input_layout.addWidget(QLabel("Funktion f(x) ="))
        input_layout.addWidget(self.function_input)
        input_layout.addWidget(self.scale_input)
        self.layout.addLayout(input_layout)
        #Instruks for korrekt anvendelse, da der ikke er tilføjet ^=opløftet, men anvender numpy direkte
        self.instruction_label = QLabel("Brug 'x' som den variable (Anvend 'x**2' fremfor 'x^2', 'math.sin(x)', 'x/10').")
        self.instruction_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.instruction_label)

        self.fire_button = QPushButton("Skyd")
        self.fire_button.clicked.connect(self.update_graph)
        self.layout.addWidget(self.fire_button)

        self.result_label = QLabel("Ram alle modstandere")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.result_label)

        
        self.setLayout(self.layout)

        # Spiltilstand, opretter lister for punkter og fjender
        self.graph_points = []
        self.enemies = []
        self.spawn_enemies()

    def spawn_enemies(self):
        # Når spillet starter eller du vil lave nye fjender
        self.enemies = [Enemy(self.width(), self.height()) for _ in range(5)]
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        w = self.width()
        h = self.height()

        # Tegn akser
        painter.setPen(QPen(Qt.white, 1))
        painter.drawLine(20, h // 2, w - 50, h // 2)  # X-akse
        painter.drawLine(w // 6, 20, w // 6, h - 150)  # Y-akse

        # Tegn graf
        if self.graph_points:
            painter.setPen(QPen(Qt.blue, 2))
            for i in range(len(self.graph_points) - 1):
                painter.drawLine(self.graph_points[i], self.graph_points[i + 1])

        # Tegn fjender
        painter.setPen(QPen(Qt.green, 2))
        for enemy in self.enemies:
            if enemy.state:
                painter.drawEllipse(QPoint(enemy.x, enemy.y), enemy.size, enemy.size)

    def update_graph(self):
        try:
            function_str = self.function_input.text().strip() #Henter funktionen fra input
            if not function_str:
                raise ValueError("Funktionen må ikke være blank")
            self.scale = float(self.scale_input.text().strip()) #Henter skalering fra input
            if not self.scale:
                raise ValueError("Funktionens skalering kan ikke være tom")
            safe_dict = {"math": math, "x": 0}
            self.graph_points = []

            w = self.width() #Nuværende bredde af skærmen
            h = self.height() #Nuværende højde af skærmen

            x_start = 50
            x_end = w - 50

            x_values = np.arange(x_start, x_end, 0.5)
            for x in x_values:
                adjusted_x = x - w // 6 #Den justerede x-akse er til venstre på skærmen (Giver større skydeplade)
                safe_dict["x"] = adjusted_x
                y = eval(function_str, {"__builtins__": {}}, safe_dict) #Omdanner tekst til matematisk udtryk (safe_dict anvendes så kode ikke kan angives og ødelægge programmet)

                screen_y = h // 2 - (y*self.scale) 
                screen_y = max(-10, min(h, screen_y))  # Hold grafen inde i området
                self.graph_points.append(QPoint(int(x), screen_y))

            """Opretter en minimum, idet enemy er opsat i et givende 
            startinterval for x-værdier, så vi ikke behøver at gennemgå hele listen af points """
            enemy_min_x = self.width() - 90
            start_index = int((enemy_min_x - 100) / 0.5)
            #Tjekker om vi rammer en fjende  
            hit_any = False
            for enemy in self.enemies:
                if enemy.state:
                    for point in self.graph_points[start_index:]:#Tjekker fra start_index og frem, sparer computerplads
                        distance = math.hypot(point.x() - enemy.x, point.y() - enemy.y) #Beregner hypotynusen hermed afstanden
                        if distance < enemy.size + 5:
                            enemy.state = False
                            hit_any = True
                            break                      
            # Opdater besked
            if all(not enemy.state for enemy in self.enemies):
                self.result_label.setText("Alle modstandere ramt, tryk enter for ny runde")
            elif hit_any:
                self.result_label.setText("Fjende ramt")
            else:
                self.result_label.setText("Ingen fjende ramt")

            self.update()
    
        except Exception as e:
            self.result_label.setText(f"Fejl: {str(e)}")
    #Ændring af størrelse på vinduet
    def resizeEvent(self, event):
        super().resizeEvent(event)
        new_width = self.width()
        new_height = self.height()
        for enemy in self.enemies:
            enemy.update_position(new_width, new_height) #Kalder opdatering af position for fjender
        self.update()

    def reset_game(self):
        self.spawn_enemies()
        self.result_label.setText("Prøv at ramme alle fjender")
        self.graph_points = []
        self.update()
#Hvis 'enter' trykkes starter spillet forfra
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.reset_game()

