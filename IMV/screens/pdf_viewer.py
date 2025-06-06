import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                               QLineEdit, QTreeView, QSplitter,
                               QFileDialog, QSizePolicy)
from PySide6.QtGui import QIcon, QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt, QUrl, QSettings, QDir
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage
import sys

# PDF læser er hentet udefra, og ændret således, det kan anvendes i programmet
# Author: BBC-Esq
# Link til Originale program: https://github.com/BBC-Esq/PySide6_PDF_Viewer/blob/main/pyside6_pdfviewer.py

class PDFFileSystemModel(QStandardItemModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHorizontalHeaderLabels(["PDF Files and Folders"])
        try:
            PATH = sys._MEIPASS  # PyInstaller
            self.root_path = os.path.join(PATH, "IMV", "screens", "PDF-Filer")
        except AttributeError:
            PATH = os.path.dirname(os.path.abspath(__file__))
            self.root_path = os.path.join(PATH, "PDF-Filer")  # Fixed to point to PDF-Filer
        print(f"PDF root path: {self.root_path}")  # Debug
        print(f"PDF directory exists: {os.path.exists(self.root_path)}")  # Debug
        self.current_path = self.root_path
        self.populate_model(self.invisibleRootItem(), self.current_path)
        
    def populate_model(self, parent_item, directory_path):
        parent_item.removeRows(0, parent_item.rowCount())
        directory = QDir(directory_path)
        up_item = QStandardItem("")
        up_item.setData(os.path.dirname(directory_path), Qt.UserRole)
        up_item.setIcon(QIcon.fromTheme("go-up"))
        parent_item.appendRow(up_item)
        directories = directory.entryInfoList(QDir.Filter.Dirs | QDir.Filter.NoDotAndDotDot, QDir.SortFlag.Name)
        for dir_info in directories:
            dir_item = QStandardItem(dir_info.fileName())
            dir_item.setData(dir_info.filePath(), Qt.UserRole)
            dir_item.setIcon(QIcon.fromTheme("folder"))
            parent_item.appendRow(dir_item)
        pdf_files = directory.entryInfoList(["*.pdf"], QDir.Filter.Files, QDir.SortFlag.Name)
        for file_info in pdf_files:
            file_item = QStandardItem(file_info.fileName())
            file_item.setData(file_info.filePath(), Qt.UserRole)
            file_item.setIcon(QIcon.fromTheme("application-pdf"))
            parent_item.appendRow(file_item)
    
    def navigate_to(self, path):
        self.current_path = path
        self.populate_model(self.invisibleRootItem(), path)

class SearchLineEdit(QLineEdit):
    def __init__(self, pdf_screen):
        super().__init__()
        self.pdf_screen = pdf_screen
    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == Qt.Key_Return:
            self.pdf_screen.search_text(self.text())

class PDFViewerScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.tree_model = PDFFileSystemModel()
        
        self.path_label = QLabel(self.tree_model.current_path)
        self.path_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.layout.addWidget(self.path_label)
        
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.layout.addWidget(self.splitter)
        
        self.nav_widget = QWidget()
        self.nav_layout = QVBoxLayout(self.nav_widget)
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.tree_model)
        self.tree_view.setHeaderHidden(True)
        self.tree_view.clicked.connect(self.on_tree_clicked)
        self.tree_view.expanded.connect(self.on_tree_expanded)
        self.nav_layout.addWidget(self.tree_view)
        self.splitter.addWidget(self.nav_widget)
        
        self.pdf_widget = QWidget()
        self.pdf_layout = QVBoxLayout(self.pdf_widget)
        self.webView = QWebEngineView()
        self.webView.settings().setAttribute(self.webView.settings().WebAttribute.PluginsEnabled, True)
        self.webView.settings().setAttribute(self.webView.settings().WebAttribute.PdfViewerEnabled, True)
        self.pdf_layout.addWidget(self.webView)
        
        self.search_input = SearchLineEdit(self)
        self.search_input.setPlaceholderText("Enter text to search...")
        self.pdf_layout.addWidget(self.search_input)
        self.splitter.addWidget(self.pdf_widget)
        self.splitter.setSizes([250, 550])
        
        self.settings = QSettings("MyCompany", "PDFViewer")
        self.recent_files = self.settings.value("recentFiles", [])

    def on_tree_clicked(self, index):
        item = self.tree_model.itemFromIndex(index)
        file_path = item.data(Qt.UserRole)
        if item.text() == "":
            self.tree_model.navigate_to(file_path)
            self.path_label.setText(file_path)
            return
        if os.path.isdir(file_path):
            self.tree_model.navigate_to(file_path)
            self.path_label.setText(file_path)
            return
        if file_path and file_path.lower().endswith('.pdf'):
            self.path_label.setText(file_path)
            pdf_url = QUrl.fromLocalFile(file_path)
            pdf_url.setFragment("zoom=page-width")
            self.webView.setUrl(pdf_url)
            self.add_to_recent_files(file_path)
    
    def on_tree_expanded(self, index):
        item = self.tree_model.itemFromIndex(index)
        file_path = item.data(Qt.UserRole)
        if item.rowCount() == 1 and item.child(0).text() == "Indlæser...":
            item.removeRow(0)
            self.tree_model.populate_model(item, file_path)
    
    def open_file_dialog(self):
        file_dialog = QFileDialog()
        filename, _ = file_dialog.getOpenFileName(self, "Åben PDF fil", "", "All Files (*)")
        if filename:
            self.load_file(filename)
    
    def load_file(self, filename):
        self.webView.setUrl(QUrl("file:///" + filename.replace('\\', '/')))
        self.add_to_recent_files(filename)
    
    def add_to_recent_files(self, filename):
        if filename in self.recent_files:
            self.recent_files.remove(filename)
        self.recent_files.insert(0, filename)
        self.recent_files = self.recent_files[:5]
        self.settings.setValue("recentFiles", self.recent_files)
    
    def search_text(self, text):
        flag = QWebEnginePage.FindFlag.FindCaseSensitively
        if text:
            self.webView.page().findText(text, flag)
        else:
            self.webView.page().stopFinding()