from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QApplication
from PySide6.QtGui import QIcon, QDrag, QDragEnterEvent, QDropEvent, QPixmap, QPainter, QPainterPath
from PySide6.QtCore import Qt, QSize, QPoint, QMimeData, QRectF
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
    def __init__(self, text, button_id, parent=None, target_screen=None, main_window=None):
        super().__init__("", parent)  # Tom tekst, da billedet fylder knappen
        self.button_id = button_id  # Unik identifikator til knappen
        self.drag_enabled = False
        self.target_screen = target_screen
        self.main_window = main_window
        self.setStyleSheet("""
            QPushButton {
                border-radius: 30px;
                background-color: #15803D;
                color: #FFFFFF;
                font-size: 14px;
                font-weight: bold;
                font-family: Arial, sans-serif;
                padding: 0px;  /* Fjern padding for at lade billedet fylde */
            }
            QPushButton:hover {
                background-color: #16A34A;
            }
            QPushButton:pressed {
                background-color: #14532D;
            }
        """)
        self.setAcceptDrops(True)
        self.clicked.connect(self.on_button_pressed)

    def set_icon(self, icon_path):
        """Sætter ikonet, tilpasser knappens størrelse til billedet og afrunder hjørnerne."""
        pixmap = QPixmap(icon_path)
        if pixmap.isNull():
            print(f"Fejl: Kunne ikke indlæse billede {icon_path}. Bruger standardstørrelse.")
            self.setFixedSize(QSize(100, 100))
            self.setIconSize(QSize(120, 60))
            self.setIcon(QIcon(icon_path))  # Forsøg alligevel at sætte ikonet
            return

        # Hent billedets dimensioner
        img_width, img_height = pixmap.width(), pixmap.height()
        
        # Maksimal størrelse for knappen
        max_width, max_height = 150, 100
        
        # Bevar billedets aspektforhold og begræns til max størrelse
        aspect_ratio = img_width / img_height
        if img_width > max_width or img_height > max_height:
            if aspect_ratio > max_width / max_height:
                # Begræns efter bredde
                img_width = max_width
                img_height = int(img_width / aspect_ratio)
            else:
                # Begræns efter højde
                img_height = max_height
                img_width = int(img_height * aspect_ratio)
        
        # Skaler pixmap til den beregnede størrelse
        pixmap = pixmap.scaled(img_width, img_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        # Opret en ny pixmap med afrundede hjørner
        rounded_pixmap = QPixmap(img_width, img_height)
        rounded_pixmap.fill(Qt.transparent)  # Gennemsigtig baggrund
        
        painter = QPainter(rounded_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Opret en afrundet rektangelsti
        path = QPainterPath()
        radius = 30  # Matcher buttonens border-radius
        path.addRoundedRect(QRectF(0, 0, img_width, img_height), radius, radius)
        
        # Klip til den afrundede sti
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()
        
        # Sæt knappens størrelse og ikon
        self.setFixedSize(QSize(img_width, img_height))
        self.setIconSize(QSize(img_width, img_height))
        self.setIcon(QIcon(rounded_pixmap))

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
            # Swap target screens, main_window og button_id
            source.target_screen, self.target_screen = self.target_screen, source.target_screen
            source.main_window, self.main_window = self.main_window, source.main_window
            source.button_id, self.button_id = self.button_id, source.button_id
            e.acceptProposedAction()

    def set_drag_enabled(self, enabled):
        self.drag_enabled = enabled

    def on_button_pressed(self):
        """Skift til den tilknyttede skærm, hvis en er defineret."""
        if self.target_screen and self.main_window:
            self.main_window.stacked_widget.setCurrentWidget(self.target_screen)
        else:
            print(f"Button {self.button_id} pressed! No target screen or main_window assigned.")

class HomeScreen(QWidget):
    """Hjemmeskærm med draggable knapper til Matematik og Kemi i en mørk-tema brugergrænseflade."""

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
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
        
        # Initialize buttons with specific screens, main_window, and button IDs
        self.buttons = [
            DraggableButton("Vektorer", "button1", self, target_screen=main_window.vector_calculator_screen, main_window=main_window),
            DraggableButton("Grafkrig", "button2", self, target_screen=main_window.game_screen, main_window=main_window),
            DraggableButton("Formler", "button3", self, target_screen=main_window.triangle_calculator_screen, main_window=main_window),
            DraggableButton("Entalpi", "button4", self, target_screen=main_window.enthalpy_screen, main_window=main_window),
            DraggableButton("PDF-viser", "button5", self, target_screen=main_window.pdf_viewer_screen, main_window=main_window),
            DraggableButton("Trekantsberegner", "button6", self, target_screen=main_window.triangle_calculator_screen, main_window=main_window),
        ]
        image_paths = ["image1.png", "image2.png", "image3.png", "image4.png", "image5.png", "image6.png"]
        for i, button in enumerate(self.buttons):
            button.set_icon(image_paths[i])  # Sæt ikon med ny metode
            button.set_drag_enabled(True)
        
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