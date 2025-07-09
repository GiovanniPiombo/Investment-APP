from PySide6.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel, QPushButton, QScrollArea, QComboBox
import sys
from ui.investment import Investment

class Advanced(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()
        self.controller()

    def setup(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.title = QLabel("Advanced Settings")
        self.title.setObjectName("advanced_title")
        self.main_layout.addWidget(self.title)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True) 
        self.scroll_content = QWidget()
        self.investment_layout = QVBoxLayout(self.scroll_content)
        self.investment_layout.setContentsMargins(2, 2, 2, 2)
        self.investment_layout.addStretch()
        self.scroll_area.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll_area)
        self.main_layout.addWidget(QLabel("Compound Frequency"))
        self.frequency = QComboBox()
        self.main_layout.addWidget(self.frequency)
        self.frequency.addItems(["Monthly","Quarterly","Semiannually","Annually"])
        self.main_layout.addWidget(QLabel("Contribution Frequency"))
        self.contribution_frequency = QComboBox()
        self.main_layout.addWidget(self.contribution_frequency)
        self.contribution_frequency.addItems(["Monthly","Quarterly","Semiannually","Annually"])

        self.addinvestment_button = QPushButton("Add Investment")
        self.main_layout.addWidget(self.addinvestment_button)


    def controller(self):
        self.addinvestment_button.clicked.connect(self.add)

    def add(self):
        investment = Investment()
        self.investment_layout.insertWidget(self.investment_layout.count()-1, investment)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Advanced()
    window.show()
    sys.exit(app.exec())
