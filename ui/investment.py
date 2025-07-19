from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QHBoxLayout
from PySide6.QtCore import QTimer
from core.ticker_thread import TickerThreadManager

class Investment(QWidget):
    """Widget to display and manage individual investment details"""
    
    def __init__(self, remove_callback=None):
        """Initialize the Investment widget"""
        super().__init__()
        self.remove_callback = remove_callback
        self.thread_manager = TickerThreadManager()
        self.current_rate = None
        self.is_analyzing = False
        
        # Timer for delayed ticker analysis (debounce)
        self.analysis_timer = QTimer()
        self.analysis_timer.setSingleShot(True)
        self.analysis_timer.timeout.connect(self._start_ticker_analysis)
        
        self.setup()
        self.setFixedHeight(320)
        self.setObjectName("InvestmentCard")

    def setup(self):
        """Set up the UI components for the Investment widget"""
        self.main_layout = QVBoxLayout(self)

        header_layout = QHBoxLayout()
        self.title = QLabel("Investment Details")
        self.title.setObjectName("advanced_details")
        header_layout.addWidget(self.title)

        if self.remove_callback:
            self.remove_btn = QPushButton("Remove")
            self.remove_btn.clicked.connect(lambda: self._cleanup_and_remove())
            header_layout.addWidget(self.remove_btn)

        self.main_layout.addLayout(header_layout)

        self.ticker = QLineEdit()
        self.ticker.setPlaceholderText("Enter ticker symbol (e.g., AAPL)")
        self.ticker.textChanged.connect(self._on_ticker_changed)
        self.main_layout.addWidget(QLabel("Ticker"))
        self.main_layout.addWidget(self.ticker)

        self.main_layout.addWidget(QLabel("Initial Deposit"))
        self.initial_deposit = QLineEdit()
        self.initial_deposit.setPlaceholderText("0.00")
        self.main_layout.addWidget(self.initial_deposit)

        self.main_layout.addWidget(QLabel("Contribution Amount"))
        self.contribution = QLineEdit()
        self.contribution.setPlaceholderText("0.00")
        self.main_layout.addWidget(self.contribution)

        # Status label for ticker analysis
        self.status_label = QLabel("")
        self.status_label.setObjectName("statusMessage")
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet("color: blue; font-style: italic;")
        self.main_layout.addWidget(self.status_label)

        # Error message label
        self.error_message = QLabel("")
        self.error_message.setObjectName("errorMessage")
        self.error_message.setWordWrap(True)
        self.error_message.setStyleSheet("color: red;")
        self.main_layout.addWidget(self.error_message)

    def _on_ticker_changed(self):
        """Handle ticker input changes with debouncing"""
        self.current_rate = None
        self.error_message.setText("")
        self.status_label.setText("")
        
        # Cancel any ongoing analysis
        if self.is_analyzing:
            self.thread_manager.cancel_all()
            self.is_analyzing = False
        
        ticker = self.ticker.text().strip()
        if ticker:
            # Use timer for debouncing (wait 1 second after user stops typing)
            self.analysis_timer.stop()
            self.analysis_timer.start(1000)  # 1 second delay

    def _start_ticker_analysis(self):
        """Start ticker analysis in background thread"""
        ticker = self.ticker.text().strip().upper()
        
        if not ticker:
            return
            
        self.is_analyzing = True
        self.status_label.setText(f"Analyzing {ticker}...")
        self.error_message.setText("")
        
        # Start analysis with callbacks
        self.thread_manager.start_analysis(
            ticker,
            result_callback=self._on_analysis_success,
            error_callback=self._on_analysis_error,
            progress_callback=self._on_analysis_progress
        )

    def _on_analysis_success(self, ticker, rate):
        """Handle successful ticker analysis"""
        self.is_analyzing = False
        self.current_rate = rate
        self.status_label.setText(f"✓ {ticker}: {rate:.2f}% annual return")
        self.status_label.setStyleSheet("color: green; font-style: italic;")
        self.error_message.setText("")

    def _on_analysis_error(self, ticker, error_message):
        """Handle ticker analysis error"""
        self.is_analyzing = False
        self.current_rate = None
        self.status_label.setText("")
        self.error_message.setText(f"Error for {ticker}: {error_message}")

    def _on_analysis_progress(self, ticker, status_message):
        """Handle ticker analysis progress updates"""
        self.status_label.setText(status_message)
        self.status_label.setStyleSheet("color: blue; font-style: italic;")

    def _cleanup_and_remove(self):
        """Clean up resources before removal"""
        self.analysis_timer.stop()
        if self.is_analyzing:
            self.thread_manager.cancel_all()
        if self.remove_callback:
            self.remove_callback(self)

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
            
            if initial_deposit < 0 or contribution < 0:
                self.error_message.setText("Amounts cannot be negative")
                return None
                
        except ValueError:
            self.error_message.setText("Please enter valid numbers for deposit and contribution")
            return None

        # Check if we have a valid rate
        if self.current_rate is None:
            if self.is_analyzing:
                self.error_message.setText("Ticker analysis in progress. Please wait...")
            else:
                self.error_message.setText("Please wait for ticker analysis to complete or enter a valid ticker")
            return None

        return {
            "ticker": self.ticker.text().strip().upper(),
            "rate": self.current_rate,
            "initial_deposit": initial_deposit,
            "contribution_amount": contribution,
            "compound_frequency": compound_freq,
            "contribution_frequency": contrib_freq,
            "years": years
        }

    def __del__(self):
        """Cleanup when widget is destroyed"""
        if hasattr(self, 'thread_manager'):
            self.thread_manager.cancel_all()
        if hasattr(self, 'analysis_timer'):
            self.analysis_timer.stop()
