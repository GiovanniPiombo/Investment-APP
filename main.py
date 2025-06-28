from ui.main_window import MainWindow
import sys
import os
from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)

    qss_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "assets/white.qss"))
    if os.path.exists(qss_path):
        with open(qss_path, "r") as f:
            app.setStyleSheet(f.read())
    else:
        print("Warning: QSS file not found at", qss_path)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())