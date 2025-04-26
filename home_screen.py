from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QApplication
from PySide6.QtGui import QIcon, QDrag, QDragEnterEvent, QDropEvent
from PySide6.QtCore import Qt, QSize, QPoint, QMimeData
from editor_screen import EditorScreen
from settings_screen import SettingsScreen
from graph_war import GraphWarScreen
from formula_collection import FormulaCollectionScreen
from pdf_viewer import PDFViewerScreen
from enthalpy_screen import EnthalpyScreen
from vector_space_screen import VectorCalculator
from triangle_calculator import TriangleCalculator

class DraggableButton(QPushButton):
    """En knap med drag-and-drop funktionalitet og design, der matcher EditorButton."""
    def __init__(self, text, parent=None, target_screen=None, main_window=None):
        super().__init__(text, parent)
        self.drag_enabled = False
        self.target_screen = target_screen  # Skærmen, knappen skal åbne
        self.main_window = main_window      # Reference til MainWindow
        self.setFixedSize(QSize(120, 60))
        self.setStyleSheet("""
            QPushButton {
                border-radius: 30px;
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
        self.setAcceptDrops(True)
        self.setIcon(QIcon("picture.png"))
        self.setIconSize(QSize(32, 32))
        
        # Connect the clicked signal to a handler
        self.clicked.connect(self.on_button_pressed)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton and self.drag_enabled:
            self.drag_start_position = e.pos()
        super().mousePressEvent(e)

    def mouseMoveEvent(self, e):
        if not (e.buttons() & Qt.LeftButton) or not self.drag_enabled:
            return
        if (e.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
        drag = QDrag(self)
        mime = QMimeData()
        drag.setMimeData(mime)
        drag.exec(Qt.MoveAction)

    def dragEnterEvent(self, e: QDragEnterEvent):
        if self.drag_enabled and isinstance(e.source(), DraggableButton):
            e.acceptProposedAction()

    def dropEvent(self, e: QDropEvent):
        if not self.drag_enabled:
            return
        source = e.source()
        if source != self and isinstance(source, DraggableButton):
            source_pos = source.pos()
            self_pos = self.pos()
            source.move(self_pos)
            self.move(source_pos)
            # Swap target screens and main_window to maintain functionality after drag-and-drop
            source.target_screen, self.target_screen = self.target_screen, source.target_screen
            source.main_window, self.main_window = self.main_window, source.main_window
            e.acceptProposedAction()

    def set_drag_enabled(self, enabled):
        self.drag_enabled = enabled

    def on_button_pressed(self):
        """Skift til den tilknyttede skærm, hvis en er defineret."""
        if self.target_screen and self.main_window:
            self.main_window.stacked_widget.setCurrentWidget(self.target_screen)
        else:
            print(f"{self.text()} pressed! No target screen or main_window assigned.")

class HomeScreen(QWidget):
    """Hjemmeskærm med draggable knapper til Matematik og Kemi i en mørk-tema brugergrænseflade."""

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window  # Reference til MainWindow for at få adgang til stacked_widget
        self.setStyleSheet("background-color: #1E1E1E;")
        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(15, 15, 15, 15)
        
        # Title
        self.title = QLabel("Velkommen til IMV!")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            font-family: Arial, sans-serif;
            color: #D1D5DB;
            padding: 8px;
        """)
        self.layout.addWidget(self.title)
        
        # Matematik container
        self.row1_container = QWidget()
        self.row1_container.setStyleSheet("background-color: #2D2D2D; border-radius: 10px;")
        self.row1_inner_layout = QVBoxLayout(self.row1_container)
        self.row1_inner_layout.setSpacing(8)
        self.row1_inner_layout.setContentsMargins(8, 8, 8, 8)
        
        self.matematik_label = QLabel("Matematik")
        self.matematik_label.setAlignment(Qt.AlignCenter)
        self.matematik_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            font-family: Arial, sans-serif;
            color: #FFFFFF;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1E3A8A, stop:1 #3B82F6);
            border-radius: 8px;
            padding: 6px;
            letter-spacing: 1px;
        """)
        self.row1_inner_layout.addWidget(self.matematik_label)
        
        self.row1_button_layout = QHBoxLayout()
        self.row1_button_layout.setSpacing(20)
        self.row1_button_layout.setAlignment(Qt.AlignCenter)
        self.row1_inner_layout.addLayout(self.row1_button_layout)
        
        # Kemi container
        self.row2_container = QWidget()
        self.row2_container.setStyleSheet("background-color: #2D2D2D; border-radius: 10px;")
        self.row2_inner_layout = QVBoxLayout(self.row2_container)
        self.row2_inner_layout.setSpacing(8)
        self.row2_inner_layout.setContentsMargins(8, 8, 8, 8)
        
        self.kemi_label = QLabel("Kemi")
        self.kemi_label.setAlignment(Qt.AlignCenter)
        self.kemi_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            font-family: Arial, sans-serif;
            color: #FFFFFF;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #14532D, stop:1 #22C55E);
            border-radius: 8px;
            padding: 6px;
            letter-spacing: 1px;
        """)
        self.row2_inner_layout.addWidget(self.kemi_label)
        
        self.row2_button_layout = QHBoxLayout()
        self.row2_button_layout.setSpacing(20)
        self.row2_button_layout.setAlignment(Qt.AlignCenter)
        self.row2_inner_layout.addLayout(self.row2_button_layout)
        
        # Initialize buttons with specific screens and main_window
        self.buttons = [
            DraggableButton("Vektorer", self, target_screen=main_window.vector_calculator_screen, main_window=main_window),
            DraggableButton("Grafkrig", self, target_screen=main_window.game_screen, main_window=main_window),
            DraggableButton("Formler", self, target_screen=main_window.formulacollection_screen, main_window=main_window),
            DraggableButton("Entalpi", self, target_screen=main_window.enthalpy_screen, main_window=main_window),
            DraggableButton("PDF-viser", self, target_screen=main_window.pdf_viewer_screen, main_window=main_window),
            DraggableButton("Trekantsberegner", self, target_screen=main_window.triangle_calculator_screen, main_window=main_window),
        ]
        image_paths = ["image1.png", "image2.png", "image3.png", "image4.png", "image5.png", "image6.png"]
        for i, button in enumerate(self.buttons):
            button.setIcon(QIcon(image_paths[i]))
            button.set_drag_enabled(True)  # Enable drag-and-drop by default
        
        # Add buttons to layouts
        for i in range(3):
            self.row1_button_layout.addWidget(self.buttons[i])
        for i in range(3, 6):
            self.row2_button_layout.addWidget(self.buttons[i])
        
        self.layout.addWidget(self.row1_container)
        self.layout.addWidget(self.row2_container)
        self.layout.addStretch()
        self.setLayout(self.layout)
        
    def toggle_drag(self, enabled):
        """Tænder eller slukker for drag-and-drop for alle knapper."""
        for button in self.buttons:
            button.set_drag_enabled(enabled)