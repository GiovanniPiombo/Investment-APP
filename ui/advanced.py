from PySide6.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QLabel, QPushButton, QComboBox, QScrollArea
from PySide6.QtCore import Signal, QTimer
from ui.investment import Investment
from core.investment_calculator import InvestmentCalculator


class Advanced(QWidget):
    investment_saved = Signal(dict)
    
    def __init__(self):
        """Initialize the Advanced settings widget"""
        super().__init__()
        self.calculator = InvestmentCalculator()
        self.setup()
        self.controller()
        
        # Timer to periodically check if all analyses are complete
        self.validation_timer = QTimer()
        self.validation_timer.setSingleShot(True)
        self.validation_timer.timeout.connect(self._check_analysis_status)
        
    def setup(self):
        """Set up the UI components for the Advanced settings"""
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)

        self._setup_title()
        self._setup_message_label()
        self._setup_years_input()
        self._setup_investments_scroll()
        self._setup_frequency_inputs()
        self._setup_buttons()

    def _setup_title(self):
        """Set up the title label"""
        self.title = QLabel("Advanced Settings")
        self.title.setObjectName("advanced_title")
        self.main_layout.addWidget(self.title)

    def _setup_message_label(self):
        """Set up the unified message label"""
        self.message = QLabel("")
        self.message.setWordWrap(True)
        self.message.setStyleSheet("")  # Start with no special styling
        self.main_layout.addWidget(self.message)

    def _setup_years_input(self):
        """Set up the years input field"""
        self.main_layout.addWidget(QLabel("Years Of Growth"))
        self.years = QLineEdit()
        self.years.setPlaceholderText("Enter number of years")
        self.main_layout.addWidget(self.years)

    def _setup_investments_scroll(self):
        """Set up the scrollable investments area"""
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(2, 2, 2, 2)
        self.scroll_layout.setSpacing(5)
        self.scroll_area.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll_area)

    def _setup_frequency_inputs(self):
        """Set up frequency selection combo boxes"""
        frequencies = self.calculator.get_available_frequencies()
        
        self.main_layout.addWidget(QLabel("Compound Frequency"))
        self.frequency = QComboBox()
        self.frequency.addItems(frequencies)
        self.main_layout.addWidget(self.frequency)

        self.main_layout.addWidget(QLabel("Contribution Frequency"))
        self.contribution_frequency = QComboBox()
        self.contribution_frequency.addItems(frequencies)
        self.main_layout.addWidget(self.contribution_frequency)

    def _setup_buttons(self):
        """Set up action buttons"""
        self.addinvestment_button = QPushButton("Add Investment")
        self.main_layout.addWidget(self.addinvestment_button)

        self.save_button = QPushButton("Save Investments")
        self.main_layout.addWidget(self.save_button)

    def controller(self):
        """Connect signals to their respective slots"""
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
        """Add a new investment widget to the scroll area"""
        investment = Investment(remove_callback=self.remove_investment)
        self.scroll_layout.addWidget(investment)
        self.show_message("Investment added successfully!")

    def remove_investment(self, widget):
        """Remove an investment widget from the scroll area"""
        self.scroll_layout.removeWidget(widget)
        widget.setParent(None)
        widget.deleteLater()
        self.show_message("Investment removed successfully!")

    def _get_analyzing_tickers(self):
        """Get list of tickers that are currently being analyzed"""
        analyzing_tickers = []
        
        for i in range(self.scroll_layout.count()):
            widget = self.scroll_layout.itemAt(i).widget()
            if isinstance(widget, Investment) and widget.is_analyzing:
                ticker = widget.ticker.text().strip().upper()
                if ticker:
                    analyzing_tickers.append(ticker)
        
        return analyzing_tickers

    def _check_analysis_status(self):
        """Check if all ticker analyses are complete"""
        analyzing_tickers = self._get_analyzing_tickers()
        
        if analyzing_tickers:
            self.show_message(f"Still analyzing: {', '.join(analyzing_tickers)}. Please wait...", is_error=True)
            # Check again in 2 seconds
            self.validation_timer.start(2000)
        else:
            # All analyses complete, try to save again
            self._perform_save()

    def _collect_investment_widgets(self):
        """Collect all Investment widgets from the scroll area"""
        widgets = []
        for i in range(self.scroll_layout.count()):
            widget = self.scroll_layout.itemAt(i).widget()
            if isinstance(widget, Investment):
                widgets.append(widget)
        return widgets

    def _validate_basic_inputs(self):
        """Validate years input and check for investments"""
        # Clear previous messages
        self.show_message("")
        
        # Validate years
        try:
            years = self.calculator.validate_years(self.years.text())
        except ValueError as e:
            self.show_message(str(e), is_error=True)
            return None
            
        # Check if there are any investments
        if self.scroll_layout.count() == 0:
            self.show_message("Please add at least one investment", is_error=True)
            return None
            
        return years

    def _check_analyzing_status(self):
        """Check if any investments are still being analyzed"""
        analyzing_tickers = self._get_analyzing_tickers()
        
        if analyzing_tickers:
            self.show_message(f"{len(analyzing_tickers)} ticker analysis(es) still in progress...", is_error=True)
            # Start timer to check status periodically
            self.validation_timer.start(2000)
            return "ANALYZING"
            
        return None

    def _collect_investments_data(self, years):
        """Collect and validate investment data from all widgets"""
        compound_freq = self.frequency.currentText()
        contrib_freq = self.contribution_frequency.currentText()
        
        investments_data = []
        investment_widgets = self._collect_investment_widgets()
        
        for widget in investment_widgets:
            data = widget.get_data(compound_freq, contrib_freq, years)
            if data is None:
                # Error message already shown by the Investment widget
                return None
            investments_data.append(data)
            
        return investments_data

    def get_investments_data(self):
        """Collect and validate investment data from the widgets"""
        # Validate basic inputs
        years = self._validate_basic_inputs()
        if years is None:
            return None
            
        # Check if analyses are still running
        analyzing_status = self._check_analyzing_status()
        if analyzing_status == "ANALYZING":
            return "ANALYZING"
            
        # Collect investment data
        investments_data = self._collect_investments_data(years)
        if investments_data is None:
            return None
            
        return investments_data, years

    def save_investments(self):
        """Save the investments data and emit the signal"""
        result = self.get_investments_data()
        
        if result is None:
            return
        elif result == "ANALYZING":
            # Analyses are still running, timer will handle retry
            return
            
        self._perform_save(result)

    def _perform_save(self, result=None):
        """Perform the actual save operation using InvestmentCalculator"""
        if result is None:
            result = self.get_investments_data()
            if result is None or result == "ANALYZING":
                return
        
        investments_data, years = result
        
        try:
            # Use the calculator to process all investments
            processed_result = self.calculator.process_investments(
                investments_data,
                self.frequency.currentText(),
                self.contribution_frequency.currentText(),
                years
            )
            
            # Emit the result
            self.investment_saved.emit(processed_result)
            self.show_message("Investments saved successfully!")
            
        except ValueError as e:
            self.show_message(str(e), is_error=True)
        except Exception as e:
            self.show_message(f"Unexpected error: {str(e)}", is_error=True)

    def cleanup(self):
        """Clean up all resources when widget is closed"""
        self.validation_timer.stop()
        
        # Clean up all investment widgets
        investment_widgets = self._collect_investment_widgets()
        for widget in investment_widgets:
            if hasattr(widget, 'thread_manager'):
                widget.thread_manager.cancel_all()

    def __del__(self):
        """Cleanup when widget is destroyed"""
        if hasattr(self, 'validation_timer'):
            self.validation_timer.stop()