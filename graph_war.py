import math
import numpy as np
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtGui import QPainter, QPen
from PySide6.QtCore import Qt, QPoint

class GraphWarScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.title = QLabel("Graph War - Hit the Target with Your Function!")
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
        self.result_label = QLabel("Try to hit the target!")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.result_label)
        self.layout.addStretch()
        self.setLayout(self.layout)
        self.target_x = 300
        self.target_y = 200
        self.graph_points = []
        self.update_graph()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 1))
        painter.drawLine(50, 400, 750, 400)
        painter.drawLine(400, 50, 400, 550)
        painter.setPen(QPen(Qt.red, 2))
        painter.drawEllipse(QPoint(self.target_x, self.target_y), 10, 10)
        if self.graph_points:
            painter.setPen(QPen(Qt.blue, 2))
            for i in range(len(self.graph_points) - 1):
                painter.drawLine(self.graph_points[i], self.graph_points[i + 1])

    def update_graph(self):
        try:
            function_str = self.function_input.text().strip()
            if not function_str:
                raise ValueError("Function cannot be empty!")
            safe_dict = {"math": math, "x": 0}
            self.graph_points = []
            x_values = np.arange(50, 751, 0.5)
            for x in x_values:
                adjusted_x = (x - 400)
                safe_dict["x"] = adjusted_x
                y = eval(function_str, {"__builtins__": {}}, safe_dict)
                screen_y = 400 - int(y)
                screen_y = max(50, min(550, screen_y))
                self.graph_points.append(QPoint(int(x), screen_y))
            min_distance = float('inf')
            for point in self.graph_points:
                distance = math.sqrt((point.x() - self.target_x)**2 + (point.y() - self.target_y)**2)
                min_distance = min(min_distance, distance)
            if min_distance < 15:
                self.result_label.setText("Hit! Target destroyed!")
            else:
                self.result_label.setText(f"Missed! Closest distance: {int(min_distance)}")
            self.update()
        except Exception as e:
            self.result_label.setText(f"Error: {str(e)}")