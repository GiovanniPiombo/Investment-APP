from PySide6.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QLabel, QPushButton, QComboBox, QScrollArea
from PySide6.QtCore import Signal
from ui.investment import Investment

class Advanced(QWidget):
    investment_saved = Signal(dict)
    
    def __init__(self):
        super().__init__()
        self.setup()
        self.controller()
        
    def setup(self):
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)

        self.title = QLabel("Advanced Settings")
        self.title.setObjectName("advanced_title")
        self.main_layout.addWidget(self.title)

        # Unified message label for both errors and success
        self.message = QLabel("")
        self.message.setWordWrap(True)
        self.message.setStyleSheet("")  # Start with no special styling
        self.main_layout.addWidget(self.message)

        self.main_layout.addWidget(QLabel("Years Of Growth"))
        self.years = QLineEdit()
        self.years.setPlaceholderText("Enter number of years")
        self.main_layout.addWidget(self.years)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(2, 2, 2, 2)
        self.scroll_layout.setSpacing(5)
        self.scroll_area.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll_area)

        self.main_layout.addWidget(QLabel("Compound Frequency"))
        self.frequency = QComboBox()
        self.frequency.addItems(["Monthly", "Quarterly", "Semiannually", "Annually"])
        self.main_layout.addWidget(self.frequency)

        self.main_layout.addWidget(QLabel("Contribution Frequency"))
        self.contribution_frequency = QComboBox()
        self.contribution_frequency.addItems(["Monthly", "Quarterly", "Semiannually", "Annually"])
        self.main_layout.addWidget(self.contribution_frequency)

        self.addinvestment_button = QPushButton("Add Investment")
        self.main_layout.addWidget(self.addinvestment_button)

        self.save_button = QPushButton("Save Investments")
        self.main_layout.addWidget(self.save_button)

    def controller(self):
        self.addinvestment_button.clicked.connect(self.add)
        self.save_button.clicked.connect(self.save_investments)

    def show_message(self, text, is_error=False):
        """Show a message with appropriate styling"""
        self.message.setText(text)
        if is_error:
            self.message.setStyleSheet("color: red;")
        else:
            self.message.setStyleSheet("color: green;")

    def add(self):
        investment = Investment(remove_callback=self.remove_investment)
        self.scroll_layout.addWidget(investment)
        self.show_message("Investment added successfully!")

    def remove_investment(self, widget):
        self.scroll_layout.removeWidget(widget)
        widget.setParent(None)
        widget.deleteLater()
        self.show_message("Investment removed successfully!")

    def get_investments_data(self):
        self.show_message("")  # Clear previous messages
        
        # Validate years input
        try:
            years = float(self.years.text().strip())
            if years <= 0:
                self.show_message("Years must be a positive number", is_error=True)
                return None
        except ValueError:
            self.show_message("Please enter valid number of years", is_error=True)
            return None

        compound_freq = self.frequency.currentText()
        contrib_freq = self.contribution_frequency.currentText()
        
        # Check if there are any investments
        if self.scroll_layout.count() == 0:
            self.show_message("Please add at least one investment", is_error=True)
            return None

        # Collect and validate all investments
        investments_data = []
        for i in range(self.scroll_layout.count()):
            widget = self.scroll_layout.itemAt(i).widget()
            if isinstance(widget, Investment):
                data = widget.get_data(compound_freq, contrib_freq, years)
                if data is None:
                    # Error message already shown by the Investment widget
                    return None
                investments_data.append(data)

        return investments_data, years

    def save_investments(self):
        result = self.get_investments_data()
        if result is None:
            return
            
        investments_data, years = result
        
        total_initial_deposit = 0.0
        total_contribution = 0.0
        weighted_rate_sum = 0.0
        total_weight = 0.0
        
        # Calculate contribution frequency multiplier
        try:
            if self.contribution_frequency.currentText() == "Monthly":
                freq = 12
            elif self.contribution_frequency.currentText() == "Quarterly":
                freq = 4
            elif self.contribution_frequency.currentText() == "Semiannually":
                freq = 2
            else:
                freq = 1
        except Exception as e:
            self.show_message(f"Error calculating frequency: {str(e)}", is_error=True)
            return

        # Process each investment
        for investment in investments_data:
            try:
                initial = float(investment["initial_deposit"])
                contrib = float(investment["contribution_amount"])
                rate = float(investment["rate"])
                
                if initial < 0 or contrib < 0:
                    raise ValueError("Negative values not allowed")
                
                total_initial_deposit += initial
                total_contribution += contrib
                
                weight = initial + (contrib * freq * years)
                weighted_rate_sum += rate * weight
                total_weight += weight
                
            except (ValueError, KeyError) as e:
                self.show_message(f"Invalid investment data: {str(e)}", is_error=True)
                return

        # Calculate weighted average rate
        try:
            if total_weight > 0:
                weighted_avg_rate = weighted_rate_sum / total_weight
            else:
                weighted_avg_rate = 0.0
        except Exception as e:
            self.show_message(f"Error calculating average rate: {str(e)}", is_error=True)
            return

        # Prepare final result
        result = {
            "rate": weighted_avg_rate,
            "initial_deposit": total_initial_deposit,
            "contribution_amount": total_contribution,
            "compound_frequency": self.frequency.currentText(),
            "contribution_frequency": self.contribution_frequency.currentText(),
            "years": years,
            "is_empty": False
        }
        
        self.investment_saved.emit(result)
        self.show_message("Investments saved successfully!")