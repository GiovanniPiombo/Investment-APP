import yfinance as yf

class TickerAnalyzer():
    def get_rate(ticker):
        data = yf.download(ticker, start="2020-01-01", end="2025-01-01")

        initial_price = float(data['Close'].iloc[0])
        final_price = float(data['Close'].iloc[-1])

        num_days = (data.index[-1] - data.index[0]).days
        num_years = num_days / 365

        cagr = (final_price / initial_price) ** (1 / num_years) - 1

        return float(cagr) * 100