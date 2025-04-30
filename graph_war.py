import math
import random
import numpy as np
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtGui import QPainter, QPen
from PySide6.QtCore import Qt, QPoint


class Enemy:
    def __init__(self, width, height):
        self.state = True  # Levende
        self.size = 10 #Størrelse (Diameter)
        self.x = random.randint(width - 60, width - 20)
        self.y = random.randint(150, height - 100)

        # Gem relativ position
        self.x_ratio = self.x / width
        self.y_ratio = self.y / height
    
    def update_position(self, new_width, new_height):
        self.x = int(self.x_ratio * new_width)
        self.y = int(self.y_ratio * new_height)
    



class GraphWarScreen(QWidget):
    def __init__(self):
        super().__init__()

        # Layout
        self.layout = QVBoxLayout()
        self.title = QLabel("Graph War - Hit the Enemies with Your Function!")
        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title)

        input_layout = QHBoxLayout()
        self.function_input = QLineEdit("x**2 / 100")
        input_layout.addWidget(QLabel("Function f(x) ="))
        input_layout.addWidget(self.function_input)
        self.layout.addLayout(input_layout)

        self.instruction_label = QLabel("Use 'x' as variable (e.g., 'x**2', 'math.sin(x)', 'x/10').")
        self.instruction_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.instruction_label)

        self.fire_button = QPushButton("Fire!")
        self.fire_button.clicked.connect(self.update_graph)
        self.layout.addWidget(self.fire_button)

        self.result_label = QLabel("Try to destroy all enemies!")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.result_label)

        self.layout.addStretch()
        self.setLayout(self.layout)

        self.scale = 1

        # Spiltilstand
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
        painter.setPen(QPen(Qt.black, 1))
        painter.drawLine(20, h // 2, w - 50, h // 2)  # X-akse
        painter.drawLine(w // 6, 20, w // 6, h - 50)  # Y-akse

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
            function_str = self.function_input.text().strip()
            if not function_str:
                raise ValueError("Function cannot be empty!")

            safe_dict = {"math": math, "x": 0}
            self.graph_points = []

            w = self.width()
            h = self.height()

            x_start = 50
            x_end = w - 50

            x_values = np.arange(x_start, x_end, 0.5)
            for x in x_values:
                adjusted_x = x - w // 6
                safe_dict["x"] = adjusted_x
                y = eval(function_str, {"__builtins__": {}}, safe_dict)

                screen_y = h // 2 - int(y*self.scale)
                screen_y = max(50, min(h - 50, screen_y))  # Hold grafen inde i området
                self.graph_points.append(QPoint(int(x), screen_y))

            # Tjek om vi rammer nogle fjender
            hit_any = False
            for enemy in self.enemies:
                if enemy.state:
                    for point in self.graph_points:
                        distance = math.hypot(point.x() - enemy.x, point.y() - enemy.y)
                        if distance < enemy.size + 5:
                            enemy.state = False
                            hit_any = True
                            break  # Stop når vi rammer én fjende

            # Opdater besked
            if all(not enemy.state for enemy in self.enemies):
                self.result_label.setText("All enemies destroyed! You win!")
            elif hit_any:
                self.result_label.setText("Enemy hit!")
            else:
                self.result_label.setText("Missed! Try again.")

            self.update()
    
        except Exception as e:
            self.result_label.setText(f"Error: {str(e)}")
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        new_width = self.width()
        new_height = self.height()
        for enemy in self.enemies:
            enemy.update_position(new_width, new_height)
        self.update()


   
    


