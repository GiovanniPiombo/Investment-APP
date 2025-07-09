from PySide6.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel, QPushButton, QLineEdit
import sys

class Investment(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        
        self.title = QLabel()
        self.title.setText("Investment Details")
        self.title.setObjectName("Advanced_Details_title")
        self.main_layout.addWidget(self.title)
        self.ticker = QLineEdit()
        self.main_layout.addWidget(QLabel("Ticker"))
        self.main_layout.addWidget(self.ticker)
        self.main_layout.addWidget(QLabel("Initial Deposit"))
        self.initial_deposit = QLineEdit()
        self.main_layout.addWidget(self.initial_deposit)
        self.main_layout.addWidget(QLabel("Contribution Amount"))
        self.contribution = QLineEdit()
        self.main_layout.addWidget(self.contribution)