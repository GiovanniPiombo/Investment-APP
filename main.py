from ui.main_window import MainWindow
import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        base_path = project_root
    
    full_path = os.path.join(base_path, relative_path)
    
    if not os.path.exists(full_path):
        script_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)
        if os.path.exists(script_dir_path):
            return script_dir_path
    
    return full_path

if __name__ == "__main__":
    app = QApplication(sys.argv)

    qss_path = get_resource_path("assets/white.qss")
    if os.path.exists(qss_path):
        with open(qss_path, "r") as f:
            app.setStyleSheet(f.read())
    else:
        print(f"Warning: QSS file not found at {qss_path}")

    window = MainWindow()
    app.setWindowIcon(QIcon(get_resource_path("assets/icon.ico")))
    window.show()
    sys.exit(app.exec())
