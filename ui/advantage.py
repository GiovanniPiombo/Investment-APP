from PySide6.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel
import sys

class Advanced(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        
        self.title = QLabel()
        self.title.setText("Advanced Settings")
        self.title.setObjectName("advanced_title")
        self.main_layout.addWidget(self.title)
        

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = Advanced()
    window.show()
    sys.exit(app.exec())