from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy, QApplication
from PySide6.QtCore import Qt
from ui.chart import Chart

class Homepage(QWidget):
    """Widget to display the homepage with investment details and chart"""

    def __init__(self):
        """Initialize the Homepage widget"""
        super().__init__()
        self.investment = {"is_empty": True}
        self.setup_ui()

    def setup_ui(self):
        """Set up the UI components for the homepage"""
        self.home_layout = QVBoxLayout()
        self.home_layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.home_layout)
        
        self.message = QLabel()
        self.message.setObjectName("home_title")
        self.home_layout.addWidget(self.message)
        
        if self.investment["is_empty"]:
            self.no_data()
        else:
            self.create_homepage()

    def no_data(self):
        """Display a message when no investment data is available"""
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

    def calculate_invested_values(self, years):
        """Calculate the invested values based on the investment data"""
        initial = self.investment['initial_deposit']
        contrib_amount = self.investment['contribution_amount']
        freq = self.investment['contribution_frequency']
        
        multiplier = {
            "Monthly": 12,
            "Quarterly": 4,
            "Semiannually": 2,
            "Annually": 1
        }[freq]
        
        yearly_contrib = contrib_amount * multiplier
        invested_values = [initial]
        
        for i in range(1, len(years)):
            invested_values.append(invested_values[-1] + yearly_contrib)
        
        return invested_values

    def create_homepage(self):
        """Create the homepage with investment details and chart"""
        self.clear_layout()
        self.message.setText("Investment Details")
        
        details_text = (
            f"Initial Deposit: ${self.investment['initial_deposit']:,.2f}\n"
            f"Years of Growth: {self.investment['years']}\n"
            f"Rate of Return: {self.investment['rate']}%\n"
            f"Compound Frequency: {self.investment['compound_frequency']}\n"
            f"Contribution Amount: ${self.investment['contribution_amount']:,.2f}\n"
            f"Contribution Frequency: {self.investment['contribution_frequency']}\n"
            f"Total Invested: ${self.investment['invested']:,.2f}\n"
            f"Final Value: ${self.investment['final_capital']:,.2f}\n"
            f"Profit: ${self.investment['profit']:,.2f}"
        )
        
        details = QLabel(details_text)
        details.setObjectName("home_details")
        
        invested_values = self.calculate_invested_values(self.years)
        
        app = QApplication.instance()
        theme = "dark" if "background-color: #121212" in app.styleSheet() else "light"
        self.chart = Chart(self.years, self.capital, invested_values, theme)
        self.chart.setObjectName("graphWidget")
        
        self.home_layout.addWidget(self.message)
        self.home_layout.addWidget(details)
        self.home_layout.addWidget(self.chart)

    def update_investment(self, new_investment, years, capital):
        """Update the homepage with new investment data"""
        self.years = years
        self.capital = capital
        self.investment = new_investment
        self.clear_layout()
        
        if not self.investment.get("is_empty", True):
            self.create_homepage()
        else:
            self.no_data()

    def clear_layout(self):
        """Clear the current layout of the homepage"""
        while self.home_layout.count():
            item = self.home_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        self.message = QLabel()
        self.message.setObjectName("home_title")
        self.home_layout.addWidget(self.message)
