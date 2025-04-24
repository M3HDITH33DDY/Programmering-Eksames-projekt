import os
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QMenu
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from home_screen import HomeScreen
from editor_screen import EditorScreen
from settings_screen import SettingsScreen
from graph_war import GraphWarScreen
from formula_collection import FormulaCollectionScreen
from pdf_viewer import PDFViewerScreen
from enthalpy_screen import EnthalpyScreen

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multi-Screen Application")
        self.setGeometry(100, 100, 800, 600)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.home_screen =akon = HomeScreen()
        self.editor_screen = EditorScreen()
        self.settings_screen = SettingsScreen()
        self.game_screen = GraphWarScreen()
        self.enthalpy_screen = EnthalpyScreen()
        self.formulacollection_screen = FormulaCollectionScreen()
        self.pdf_viewer_screen = PDFViewerScreen()

        self.stacked_widget.addWidget(self.home_screen)
        self.stacked_widget.addWidget(self.editor_screen)
        self.stacked_widget.addWidget(self.settings_screen)
        self.stacked_widget.addWidget(self.enthalpy_screen)
        self.stacked_widget.addWidget(self.game_screen)
        self.stacked_widget.addWidget(self.formulacollection_screen)
        self.stacked_widget.addWidget(self.pdf_viewer_screen)

        self.create_menu_bar()

    def create_menu_bar(self):
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu("File")
        
        home_action = QAction("Home", self)
        home_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.home_screen))
        file_menu.addAction(home_action)

        editor_action = QAction("Text Editor", self)
        editor_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.editor_screen))
        file_menu.addAction(editor_action)

        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.settings_screen))
        file_menu.addAction(settings_action)

        enthalpy_action = QAction("Entalpi Beregner", self)
        enthalpy_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.enthalpy_screen))
        file_menu.addAction(enthalpy_action)

        game_action = QAction("Graph War", self)
        game_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.game_screen))
        file_menu.addAction(game_action)

        formula_collection = QAction("Formelsamling", self)
        formula_collection.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.formulacollection_screen))
        file_menu.addAction(formula_collection)

        pdf_viewer_action = QAction("PDF Viewer", self)
        pdf_viewer_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.pdf_viewer_screen))
        file_menu.addAction(pdf_viewer_action)

        open_pdf_action = QAction("Open PDF", self)
        open_pdf_action.triggered.connect(self.pdf_viewer_screen.open_file_dialog)
        file_menu.addAction(open_pdf_action)

        recent_menu = QMenu("Recent PDFs", self)
        file_menu.addMenu(recent_menu)
        self.update_recent_files_menu(recent_menu)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        formula_menu = menubar.addMenu("Formula Collection")
        x_squared = QAction("x²", self)
        x_squared.triggered.connect(lambda: self.game_screen.function_input.setText("x**2 / 100"))
        formula_menu.addAction(x_squared)

        x_cubed = QAction("x³", self)
        x_cubed.triggered.connect(lambda: self.game_screen.function_input.setText("x**3 / 1000"))
        formula_menu.addAction(x_cubed)

        x_to_four = QAction("x⁴", self)
        x_to_four.triggered.connect(lambda: self.game_screen.function_input.setText("x**4 / 10000"))
        formula_menu.addAction(x_to_four)

        sine_x = QAction("sin(x)", self)
        sine_x.triggered.connect(lambda: self.game_screen.function_input.setText("math.sin(x / 50)"))
        formula_menu.addAction(sine_x)

    def update_recent_files_menu(self, recent_menu):
        recent_menu.clear()
        for file in self.pdf_viewer_screen.recent_files:
            action = QAction(os.path.basename(file), self)
            action.setData(file)
            action.triggered.connect(lambda checked, f=file: self.pdf_viewer_screen.load_file(f))
            recent_menu.addAction(action)