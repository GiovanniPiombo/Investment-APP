from PySide6.QtWidgets import QWidget, QVBoxLayout, QStackedLayout, QPushButton, QSpacerItem, QSizePolicy, QLineEdit, QLabel, QHBoxLayout, QComboBox
from PySide6.QtCore import Signal

class Portfolio(QWidget):
    investment_saved = Signal(dict)
    def __init__(self):
        super().__init__()
        self.investment = {
            "is_empty" : True
        }
        self.make_settings()
        self.controller()

    def make_settings(self):
        self.settings_layout = QVBoxLayout()
        self.settings_layout.setContentsMargins(20, 20, 20, 20)
        self.settings_layout.setSpacing(10)
        self.portfolio_title = QLabel("Your Investments")
        self.settings_layout.addWidget(self.portfolio_title)
        self.portfolio_title.setObjectName("portfolio_title")
        self.settings_layout.addWidget(QLabel("Initial Deposit"))
        self.initial_deposit = QLineEdit()
        self.settings_layout.addWidget(self.initial_deposit)
        self.settings_layout.addWidget(QLabel("Years Of Growth"))
        self.years = QLineEdit()
        self.settings_layout.addWidget(self.years)
        self.settings_layout.addWidget(QLabel("Estimated Rate Of Return (%)"))
        self.rate = QLineEdit()
        self.settings_layout.addWidget(self.rate)
        self.settings_layout.addWidget(QLabel("Compound Frequency"))
        self.frequency = QComboBox()
        self.settings_layout.addWidget(self.frequency)
        self.frequency.addItems(["Monthly","Quarterly","Semiannually","Annually"])
        self.settings_layout.addWidget(QLabel("Contribution Amount"))
        self.contribution = QLineEdit()
        self.settings_layout.addWidget(self.contribution)
        self.settings_layout.addWidget(QLabel("Contribution Frequency"))
        self.contribution_frequency = QComboBox()
        self.contribution_frequency.addItems(["Monthly","Quarterly","Semiannually","Annually"])
        self.settings_layout.addWidget(self.contribution_frequency)
        self.save_button = QPushButton("Save")
        self.settings_layout.addWidget(self.save_button)
        self.message = QLabel("")
        self.warning = QLabel("")
        self.settings_layout.addWidget(self.message)
        self.settings_layout.addWidget(self.warning)
        self.setLayout(self.settings_layout)
        
    def controller(self):
        self.save_button.clicked.connect(self.save_investment)

    def save_investment(self):
        self.warning.setText("")
        is_ok = True

        try:
            initial_deposit = float(self.initial_deposit.text())
            if initial_deposit < 0:
                is_ok = False
                self.error_message("Initial Deposit cannot be negative!")
        except ValueError:
            is_ok = False
            self.error_message("Initial Deposit!")

        try:
            years = float(self.years.text())
            if years < 0:
                is_ok = False
                self.error_message("Years Of Growth cannot be negative!")
        except ValueError:
            is_ok = False
            self.error_message("Years Of Growth!")

        try:
            rate = float(self.rate.text())
            if rate < 0:
                self.warning_message("negative interest rate will cause loss!")
            elif rate > 100:
                self.warning_message("unrealistic interest rate!")

        except ValueError:
            is_ok = False
            self.error_message("Interest Rate!")

        try:
            contribution = float(self.contribution.text())
            if contribution < 0:
                is_ok = False
                self.error_message("Contribution Amount cannot be negative!")
        except ValueError:
            is_ok = False
            self.error_message("Contribution Amount!")

        if is_ok:
            self.message.setText("Investment Saved")
            self.message.setStyleSheet("color : green")
            self.investment.update({
                "initial_deposit" : initial_deposit,
                "years" : years,
                "rate" : rate,
                "compound_frequency" : self.frequency.currentText(),
                "contribution_amount" : contribution,
                "contribution_frequency" : self.contribution_frequency.currentText(),
                "is_empty" : False
            })
            self.investment_saved.emit(self.investment)
    
    def error_message(self, text):
        self.message.setText("Error : " + text)
        self.message.setStyleSheet("color : red")

    def warning_message(self, text):
        self.warning.setText("Warning : " + text)
        self.warning.setStyleSheet("color : orange")