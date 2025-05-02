import sys
import traceback
from PySide6.QtWidgets import QApplication, QMessageBox
from main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    #Fejl ved opstart, til exe, ikke under udvikling
    """try:
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        error_msg = traceback.format_exc()
        QMessageBox.critical(None, "Fatal Error", f"An unexpected error occurred:\n{error_msg}")
        sys.exit(1)"""

if __name__ == "__main__":
    main()
