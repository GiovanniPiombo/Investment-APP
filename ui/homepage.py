from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt

class Homepage(QWidget):
    def __init__(self):
        super().__init__()
        self.investment = {"is_empty": True}

        self.home_layout = QVBoxLayout()
        self.home_layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.home_layout)

        self.message = QLabel()
        self.home_layout.addWidget(self.message)
        self.message.setObjectName("home_title")

        if self.investment["is_empty"]:
            self.no_data()
        else:
            self.create_homepage()

    def no_data(self):
        self.message.setText("No Investment Data Found")
    
        instructions = QLabel(
        "👋 Start your investment journey!\n\n"
        "1. Click on 'Portfolio' in the sidebar\n"
        "2. Fill in your financial details\n"
        "3. See your growth projections here"
    )
        instructions.setObjectName("home_instructions")
        instructions.setAlignment(Qt.AlignCenter)
    
        self.home_layout.addWidget(instructions)
    
        self.home_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def create_homepage(self):
        self.clear_layout()

        self.message.setText("Investment Details")
        self.home_layout.addWidget(self.message)

        details = QLabel(
            f"Initial Deposit: {self.investment['initial_deposit']}\n"
            f"Years of Growth: {self.investment['years']}\n"
            f"Rate of Return: {self.investment['rate']}%\n"
            f"Compound Frequency: {self.investment['compound_frequency']}\n"
            f"Contribution Amount: {self.investment['contribution_amount']}\n"
            f"Contribution Frequency: {self.investment['contribution_frequency']}\n"
            f"Invested: {self.investment['invested']}\n"
            f"Final Capital: {self.investment['final_capital']}\n"
            f"Profit: {self.investment['profit']}\n"
        )
        self.home_layout.addWidget(details)
        details.setObjectName("home_details")

    def update_investment(self, new_investment):
        self.investment = new_investment
        self.clear_layout()
        if not self.investment.get("is_empty", True):
            self.create_homepage()
        else:
            self.no_data()

    def clear_layout(self):
        # Rimuove tutto dal layout
        while self.home_layout.count():
            item = self.home_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Ricrea message vuoto
        self.message = QLabel()
        self.message.setObjectName("home_title")
        self.home_layout.addWidget(self.message)
