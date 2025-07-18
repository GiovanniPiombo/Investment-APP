import time
from urllib.request import urlopen
from urllib.error import URLError
import yfinance as yf

class TickerAnalyzer:
    @staticmethod
    def is_internet_available():
        """Check if internet connection is available."""
        try:
            urlopen('https://www.google.com', timeout=5)
            return True
        except URLError:
            return False

    @staticmethod
    def get_rate(ticker, max_retries=3, retry_delay=5):
        """
        Calculate the Compound Annual Growth Rate (CAGR) for a given stock ticker.
        """
        if not isinstance(ticker, str) or not ticker.strip():
            raise ValueError("Ticker must be a non-empty string")
        if not isinstance(max_retries, int) or max_retries < 0:
            raise ValueError("max_retries must be a non-negative integer")
        if not isinstance(retry_delay, (int, float)) or retry_delay < 0:
            raise ValueError("retry_delay must be a non-negative number")

        attempts = 0
        last_exception = None

        while attempts <= max_retries:
            attempts += 1
            try:
                if not TickerAnalyzer.is_internet_available():
                    if attempts <= max_retries:
                        print(f"No internet connection. Retrying in {retry_delay} seconds... (Attempt {attempts}/{max_retries})")
                        time.sleep(retry_delay)
                        continue
                    else:
                        raise Exception("No internet connection after maximum retries")

                try:
                    data = yf.download(ticker, start="2020-01-01", end="2025-01-01", progress=False)
                except Exception as e:
                    if "No timezone found" in str(e):
                        raise
                    if attempts <= max_retries:
                        print(f"Download failed. Retrying in {retry_delay} seconds... (Attempt {attempts}/{max_retries})")
                        time.sleep(retry_delay)
                        continue
                    else:
                        raise Exception(f"Failed to download data after {max_retries} attempts: {str(e)}")

                if data.empty:
                    raise ValueError(f"No data available for ticker {ticker}")
                if len(data) < 2:
                    raise ValueError(f"Insufficient data points for ticker {ticker}")

                initial_price = float(data['Close'].iloc[0])
                final_price = float(data['Close'].iloc[-1])
                if initial_price <= 0 or final_price <= 0:
                    raise ValueError("Prices must be positive values")

                num_days = (data.index[-1] - data.index[0]).days
                if num_days <= 0:
                    raise ValueError("Invalid date range in data")
                num_years = num_days / 365

                if initial_price == 0:
                    raise ValueError("Initial price cannot be zero")

                cagr = (final_price / initial_price) ** (1 / num_years) - 1
                return float(cagr) * 100

            except Exception as e:
                last_exception = e
                if attempts <= max_retries:
                    print(f"Attempt {attempts} failed. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    raise last_exception
