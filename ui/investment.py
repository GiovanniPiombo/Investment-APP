from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QHBoxLayout
from core.ticker_analyzer import TickerAnalyzer
class Investment(QWidget):
    def __init__(self, remove_callback=None):
        super().__init__()
        self.remove_callback = remove_callback
        self.setup()
        self.setFixedHeight(320)
        self.setObjectName("InvestmentCard")

    def setup(self):
        self.main_layout = QVBoxLayout(self)

        header_layout = QHBoxLayout()
        self.title = QLabel("Investment Details")
        self.title.setObjectName("advanced_details")
        header_layout.addWidget(self.title)

        if self.remove_callback:
            self.remove_btn = QPushButton("Remove")
            self.remove_btn.clicked.connect(lambda: self.remove_callback(self))
            header_layout.addWidget(self.remove_btn)

        self.main_layout.addLayout(header_layout)

        self.ticker = QLineEdit()
        self.main_layout.addWidget(QLabel("Ticker"))
        self.main_layout.addWidget(self.ticker)

        self.main_layout.addWidget(QLabel("Initial Deposit"))
        self.initial_deposit = QLineEdit()
        self.main_layout.addWidget(self.initial_deposit)

        self.main_layout.addWidget(QLabel("Contribution Amount"))
        self.contribution = QLineEdit()
        self.main_layout.addWidget(self.contribution)

    def get_data(self, compound_freq, contrib_freq, years):
        rate = TickerAnalyzer.get_rate(self.ticker.text())
        return {
        "ticker": self.ticker.text(),
        "rate": rate,
        "initial_deposit": self.initial_deposit.text(),
        "contribution_amount": self.contribution.text(),
        "compound_frequency": compound_freq,
        "contribution_frequency": contrib_freq,
        "years": years
        }