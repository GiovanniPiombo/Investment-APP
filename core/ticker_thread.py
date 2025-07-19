from PySide6.QtCore import QThread, Signal
from core.ticker_analyzer import TickerAnalyzer

class TickerWorker(QThread):
    """Worker thread for ticker analysis without blocking the UI"""
    
    # Signals to communicate with the main thread
    result_ready = Signal(str, float)  # ticker, rate
    error_occurred = Signal(str, str)  # ticker, error_message
    progress_update = Signal(str, str)  # ticker, status_message
    
    def __init__(self, ticker, max_retries=2, retry_delay=2):
        super().__init__()
        self.ticker = ticker
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self._is_cancelled = False
    
    def run(self):
        """Execute ticker analysis in background"""
        if self._is_cancelled:
            return
            
        try:
            self.progress_update.emit(self.ticker, f"Analyzing ticker {self.ticker}...")
            
            # Call TickerAnalyzer with reduced parameters to avoid long freezes
            rate = TickerAnalyzer.get_rate(
                self.ticker, 
                max_retries=self.max_retries, 
                retry_delay=self.retry_delay
            )
            
            if not self._is_cancelled:
                self.result_ready.emit(self.ticker, rate)
                
        except Exception as e:
            if not self._is_cancelled:
                error_msg = str(e)
                # Customize error messages for user
                if "No data available" in error_msg:
                    error_msg = f"Ticker '{self.ticker}' not found or has no data"
                elif "No internet connection" in error_msg:
                    error_msg = "No internet connection available"
                elif "Failed to download data" in error_msg:
                    error_msg = f"Failed to retrieve data for '{self.ticker}'"
                
                self.error_occurred.emit(self.ticker, error_msg)
    
    def cancel(self):
        """Cancel the operation"""
        self._is_cancelled = True
        self.requestInterruption()

class TickerThreadManager:
    """Manager to handle multiple ticker requests"""
    
    def __init__(self):
        self.active_workers = {}  # ticker -> worker
        
    def start_analysis(self, ticker, result_callback=None, error_callback=None, progress_callback=None):
        """Start analysis of a ticker"""
        ticker = ticker.strip().upper()
        
        # If there's already an analysis running for this ticker, cancel it
        if ticker in self.active_workers:
            self.cancel_analysis(ticker)
        
        # Create and start the worker
        worker = TickerWorker(ticker, max_retries=2, retry_delay=2)
        
        # Connect callbacks if provided
        if result_callback:
            worker.result_ready.connect(result_callback)
        if error_callback:
            worker.error_occurred.connect(error_callback)
        if progress_callback:
            worker.progress_update.connect(progress_callback)
            
        # Automatic cleanup when thread finishes
        worker.finished.connect(lambda: self._cleanup_worker(ticker))
        
        self.active_workers[ticker] = worker
        worker.start()
        
        return worker
    
    def cancel_analysis(self, ticker):
        """Cancel analysis of a specific ticker"""
        ticker = ticker.upper()
        if ticker in self.active_workers:
            worker = self.active_workers[ticker]
            worker.cancel()
            worker.wait(1000)  # Wait max 1 second
            if worker.isRunning():
                worker.terminate()
            self._cleanup_worker(ticker)
    
    def cancel_all(self):
        """Cancel all ongoing analyses"""
        for ticker in list(self.active_workers.keys()):
            self.cancel_analysis(ticker)
    
    def _cleanup_worker(self, ticker):
        """Remove worker from active list"""
        if ticker in self.active_workers:
            del self.active_workers[ticker]
    
    def is_analyzing(self, ticker):
        """Check if a ticker is currently being analyzed"""
        return ticker.upper() in self.active_workers
