import pytest
from unittest.mock import patch
import pandas as pd
from datetime import datetime
import sys
import os
from urllib.error import URLError

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.ticker_analyzer import TickerAnalyzer

@pytest.fixture
def mock_yfinance_data():
    date_range = pd.date_range(start="2020-01-01", end="2025-01-01", freq="D")
    return pd.DataFrame({
        'Close': [100 * (1.1 ** i) for i in range(len(date_range))]
    }, index=date_range)

class TestInternetCheck:
    @patch('core.ticker_analyzer.urlopen')
    def test_is_internet_available_success(self, mock_urlopen):
        mock_urlopen.return_value = True
        assert TickerAnalyzer.is_internet_available() is True

    @patch('core.ticker_analyzer.urlopen', side_effect=URLError('No connection'))
    def test_is_internet_available_failure(self, mock_urlopen):
        assert TickerAnalyzer.is_internet_available() is False

class TestGetRate:
    @pytest.mark.parametrize("ticker, max_retries, retry_delay, expected_error", [
        ("", 3, 5, "Ticker must be a non-empty string"),
        (None, 3, 5, "Ticker must be a non-empty string"),
        ("AAPL", -1, 5, "max_retries must be a non-negative integer"),
        ("AAPL", 3, -1, "retry_delay must be a non-negative number"),
    ])
    def test_invalid_inputs(self, ticker, max_retries, retry_delay, expected_error):
        with pytest.raises(ValueError) as excinfo:
            TickerAnalyzer.get_rate(ticker, max_retries, retry_delay)
        assert expected_error in str(excinfo.value)

    @patch('core.ticker_analyzer.TickerAnalyzer.is_internet_available', return_value=False)
    @patch('time.sleep')
    def test_no_internet_connection(self, mock_sleep, mock_internet):
        with pytest.raises(Exception, match="No internet connection after maximum retries"):
            TickerAnalyzer.get_rate("AAPL", max_retries=2, retry_delay=1)
        assert mock_sleep.call_count == 2

    @patch('core.ticker_analyzer.TickerAnalyzer.is_internet_available', return_value=True)
    @patch('yfinance.download', side_effect=Exception("Download failed"))
    @patch('time.sleep')
    def test_download_failure(self, mock_sleep, mock_download, mock_internet):
        with pytest.raises(Exception, match="Download failed"):
            TickerAnalyzer.get_rate("AAPL", max_retries=1)
        assert mock_download.called

    @patch('core.ticker_analyzer.TickerAnalyzer.is_internet_available', return_value=True)
    @patch('yfinance.download', return_value=pd.DataFrame())
    def test_empty_data(self, mock_download, mock_internet):
        with pytest.raises(ValueError, match="No data available"):
            TickerAnalyzer.get_rate("AAPL")

    @patch('core.ticker_analyzer.TickerAnalyzer.is_internet_available', return_value=True)
    @patch('yfinance.download', return_value=pd.DataFrame({'Close': [100]}))
    def test_insufficient_data(self, mock_download, mock_internet):
        with pytest.raises(ValueError, match="Insufficient data points"):
            TickerAnalyzer.get_rate("AAPL")

    @patch('core.ticker_analyzer.TickerAnalyzer.is_internet_available', return_value=True)
    def test_successful_cagr_calculation(self, mock_internet, mock_yfinance_data):
        with patch('yfinance.download', return_value=mock_yfinance_data):
            result = TickerAnalyzer.get_rate("AAPL")
            assert isinstance(result, float)
            assert result > 0

    @patch('core.ticker_analyzer.TickerAnalyzer.is_internet_available', return_value=True)
    def test_zero_initial_price(self, mock_internet):
        """Test handling of zero initial price edge case"""
        test_data = pd.DataFrame({
            'Close': [0, 100]  # Zero initial price
        }, index=[datetime(2020,1,1), datetime(2021,1,1)])
    
        with patch('yfinance.download', return_value=test_data):
            with pytest.raises(ValueError, match="Prices must be positive values"):
                TickerAnalyzer.get_rate("AAPL")


    @patch('core.ticker_analyzer.TickerAnalyzer.is_internet_available', side_effect=[False, True])
    def test_retry_success(self, mock_internet, mock_yfinance_data):
        with patch('yfinance.download', return_value=mock_yfinance_data), \
             patch('time.sleep'):
            result = TickerAnalyzer.get_rate("AAPL", max_retries=2)
            assert isinstance(result, float)
            assert mock_internet.call_count == 2

@pytest.mark.integration
class TestIntegration:
    def test_real_ticker(self):
        result = TickerAnalyzer.get_rate("AAPL")
        assert result is None or isinstance(result, float)
