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

        self.error_message = QLabel("")
        self.error_message.setObjectName("errorMessage")  # Add this for CSS styling
        self.error_message.setWordWrap(True)  # Ensure long messages wrap
        self.error_message.setStyleSheet("color: red;")  # Make errors stand out
        self.main_layout.addWidget(self.error_message)

    def get_data(self, compound_freq, contrib_freq, years):
        """Get investment data with error handling and message display"""
        self.error_message.setText("")  # Clear previous errors
        
        # Validate required fields
        if not self.ticker.text().strip():
            self.error_message.setText("Please enter a ticker symbol")
            return None
            
        if not self.initial_deposit.text().strip():
            self.error_message.setText("Please enter an initial deposit amount")
            return None
            
        if not self.contribution.text().strip():
            self.error_message.setText("Please enter a contribution amount")
            return None

        # Validate numeric fields
        try:
            initial_deposit = float(self.initial_deposit.text())
            contribution = float(self.contribution.text())
        except ValueError:
            self.error_message.setText("Please enter valid numbers for deposit and contribution")
            return None

        # Get rate from TickerAnalyzer
        rate = TickerAnalyzer.get_rate(self.ticker.text())
        
        if rate is None:
            # The error message is already set by TickerAnalyzer
            self.error_message.setText("Failed to get rate for this ticker. Please check the symbol and try again.")
            return None

        return {
            "ticker": self.ticker.text().strip().upper(),
            "rate": rate,
            "initial_deposit": initial_deposit,
            "contribution_amount": contribution,
            "compound_frequency": compound_freq,
            "contribution_frequency": contrib_freq,
            "years": years
        }