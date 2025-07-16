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

        self.main_layout.addWidget(QLabel("Years Of Growth"))
        self.years = QLineEdit()
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

    def add(self):
        investment = Investment(remove_callback=self.remove_investment)
        self.scroll_layout.addWidget(investment)

    def remove_investment(self, widget):
        self.scroll_layout.removeWidget(widget)
        widget.setParent(None)
        widget.deleteLater()

    def get_investments_data(self):
        investments_data = []
        compound_freq = self.frequency.currentText()
        contrib_freq = self.contribution_frequency.currentText()
        years = self.years.text()
    
        for i in range(self.scroll_layout.count()):
            widget = self.scroll_layout.itemAt(i).widget()
            if isinstance(widget, Investment):
                investments_data.append(widget.get_data(compound_freq, contrib_freq, years))
        return investments_data

    def save_investments(self):
        investments_data = self.get_investments_data()
    
        if not investments_data:
            return None
    
        total_initial_deposit = 0.0
        total_contribution = 0.0
        weighted_rate_sum = 0.0
        total_weight = 0.0
    
        try:
            years = float(self.years.text())
        except ValueError:
            print("Invalid years value")
            return None
        
        if(self.contribution_frequency.currentText() == "Monthly"):
            freq = 12
        elif(self.contribution_frequency.currentText() == "Quarterly"):
            freq = 4
        elif(self.contribution_frequency.currentText() == "Semiannually"):
            freq = 2
        else:
            freq = 1
        
        for investment in investments_data:
            try:
                initial = float(investment["initial_deposit"])
                contrib = float(investment["contribution_amount"])
                rate = float(investment["rate"])
            
                total_initial_deposit += initial
                total_contribution += contrib
            
                weight = initial + (contrib * freq * years)
                weighted_rate_sum += rate * weight
                total_weight += weight
            
            except (ValueError, KeyError) as e:
                print(f"Error processing investment data: {e}")
                continue
    
        if total_weight > 0:
            weighted_avg_rate = weighted_rate_sum / total_weight
        else:
            weighted_avg_rate = 0.0
    
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