import os
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QMenu
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from home_screen import (HomeScreen, VectorCalculator, EnthalpyScreen, PDFViewerScreen, 
                         GraphWarScreen, EditorScreen, SettingsScreen, TriangleCalculator)

class MainWindow(QMainWindow):
    """Hovedvindue til at navigere mellem forskellige skærme i en mørk-tema brugergrænseflade."""

    def __init__(self):
        super().__init__()
        # mørk tema for menubar
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1E1E1E;
            }
            QMenuBar {
                background-color: #2D2D2D;
                color: #FFFFFF;
                font-family: Arial, sans-serif;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
            }
            QMenuBar::item {
                background-color: #2D2D2D;
                color: #FFFFFF;
                padding: 5px 10px;
                border-radius: 8px;
            }
            QMenuBar::item:selected {
                background-color: #16A34A;
            }
            QMenuBar::item:pressed {
                background-color: #14532D;
            }
            QMenu {
                background-color: #2D2D2D;
                color: #FFFFFF;
                font-family: Arial, sans-serif;
                font-size: 14px;
                font-weight: bold;
                border: 1px solid #4B5563;
                border-radius: 8px;
            }
            QMenu::item {
                padding: 5px 20px;
                border-radius: 8px;
            }
            QMenu::item:selected {
                background-color: #16A34A;
                color: #FFFFFF;
            }
            QMenu::item:pressed {
                background-color: #14532D;
            }
        """)
        self.setWindowTitle("Multi Program")
        self.setGeometry(100, 100, 1200, 600)

        # Central wiget
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background-color: #1E1E1E;")
        self.setCentralWidget(self.stacked_widget)

        # Initialisering af skærme
        self.editor_screen = EditorScreen()
        self.settings_screen = SettingsScreen()
        self.game_screen = GraphWarScreen()
        self.enthalpy_screen = EnthalpyScreen()
        self.pdf_viewer_screen = PDFViewerScreen()
        self.vector_calculator_screen = VectorCalculator()
        self.triangle_calculator_screen = TriangleCalculator()
        self.home_screen = HomeScreen(self)  

        # Tilføj skærme til knapperne
        self.stacked_widget.addWidget(self.home_screen)
        self.stacked_widget.addWidget(self.editor_screen)
        self.stacked_widget.addWidget(self.settings_screen)
        self.stacked_widget.addWidget(self.enthalpy_screen)
        self.stacked_widget.addWidget(self.game_screen)
        self.stacked_widget.addWidget(self.pdf_viewer_screen)
        self.stacked_widget.addWidget(self.vector_calculator_screen)
        self.stacked_widget.addWidget(self.triangle_calculator_screen)

        # Fremstilling af menubar
        self.create_menu_bar()

    def create_menu_bar(self):
        """Opretter menubjælken med navigationsmuligheder til forskellige skærme."""
        menubar = self.menuBar()

        # Fil menu
        file_menu = menubar.addMenu("Fil")

        home_action = QAction("Hjem", self)
        home_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.home_screen))
        file_menu.addAction(home_action)

        editor_action = QAction("Teksteditor", self)
        editor_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.editor_screen))
        file_menu.addAction(editor_action)

        settings_action = QAction("Indstillinger", self)
        settings_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.settings_screen))
        file_menu.addAction(settings_action)

        enthalpy_action = QAction("Entalpi Beregner", self)
        enthalpy_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.enthalpy_screen))
        file_menu.addAction(enthalpy_action)

        game_action = QAction("Grafkrig", self)
        game_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.game_screen))
        file_menu.addAction(game_action)

        pdf_viewer_action = QAction("PDF-viser", self)
        pdf_viewer_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.pdf_viewer_screen))
        file_menu.addAction(pdf_viewer_action)

        open_pdf_action = QAction("Åbn PDF", self)
        open_pdf_action.triggered.connect(self.pdf_viewer_screen.open_file_dialog)
        file_menu.addAction(open_pdf_action)

        exit_action = QAction("Afslut", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Math menu
        math_menu = menubar.addMenu("Matematik")
        vector_action = QAction("Vektorer", self)
        vector_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.vector_calculator_screen))
        math_menu.addAction(vector_action)

        triangle_action = QAction("Trekantsberegner", self)
        triangle_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.triangle_calculator_screen))
        math_menu.addAction(triangle_action)

        # Chemistry menu
        chemistry_menu = menubar.addMenu("Kemi")
        enthalpy_screen_action = QAction("Entalpi Beregner", self)
        enthalpy_screen_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.enthalpy_screen))
        chemistry_menu.addAction(enthalpy_screen_action)

        