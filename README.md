# 💼 Investment App

**Investment App** is a desktop application built with **PySide6** that allows users to simulate and track the growth of their investments over time. It features a clean and intuitive interface with modular pages for portfolio input, advanced simulations, and a summary dashboard.

---

## 🚀 Features

- 📊 **Portfolio Input**  
  Enter initial deposit, interest rate, contribution frequency, and other key parameters.

- 🧠 **Advanced Ticker-Based Simulation**  
  Analyze multiple **stock tickers** (e.g., AAPL, TSLA) with automatic data fetching from **Yahoo Finance**:
  - Calculates **historical CAGR** (2020–2025)
  - Supports weighted average across multiple tickers
  - Gracefully handles invalid or unavailable tickers

- 🏠 **Homepage Summary**  
  View a detailed breakdown of your investment projections and total returns.

- 📈 **Interactive Growth Chart**  
  Visual comparison between:
  - Compound growth  
  - Linear total investment  
  - Light/dark theme-aware design

- 🎚️ **Chart Controls**  
  - Mouse wheel: Zoom  
  - Click + drag: Pan  
  - Double-click: Reset view  
  - Rubber-band: Zoom to selected area

- ⚙️ **Theme Settings**  
  Easily switch between light and dark modes using `.qss` stylesheets.

- 🧩 **Modular Architecture**  
  Component-based structure with clear signal-slot communication.

- 🖼️ **Custom App Icon**  
  Includes a personalized `icon.ico` for a polished experience.

- 💾 **Windows Setup (.exe)**  
  The app can be installed as a standalone Windows executable — no Python installation required.

---

## 🧩 Project Structure

```
project/
├── assets/
│   ├── white.qss                     # Light theme stylesheet
│   ├── dark.qss                      # Dark theme stylesheet
│   └── icon.ico                      # App icon
├── core/
│   ├── ticker_analyzer.py            # Ticker CAGR logic
│   ├── investment_calculator.py      # Investment portfolio aggregation and weighted calculations
│   ├── finance.py                    # Core financial calculations
│   └── ticker_thread.py              # Asynchronous ticker analysis with threading
├── ui/
│   ├── chart.py                      # Investment growth chart
│   ├── homepage.py                   # Summary display
│   ├── main_window.py                # Main app window
│   ├── portfolio.py                  # Portfolio input page
│   ├── advanced.py                   # Advanced multi-ticker input
│   ├── investment.py                 # Investment input component
│   └── settings.py                   # Theme and settings page
├── tests/
│   ├── conftest.py                   # Test configs
│   ├── test_finance.py               # Finance Test
│   ├── test_ticker_analyzer.py       # Ticker Analyzer Test
│   └── test_investment_calculator.py # Investment calculator comprehensive tests
├── main.py                           # App entry point
├── README.md                         # This file
├── requirements.txt                  # Dependencies
└── InvestmentApp.spec                # PyInstaller build config
```

---

## 🛠️ How to Run

1️⃣ Clone the repository:

```bash
git clone https://github.com/GiovanniPiombo/Investment-APP.git
cd Investment-APP
```

2️⃣ Install the dependencies:

```bash
pip install -r requirements.txt
```

3️⃣ Launch the application:

```bash
python main.py
```

---

## 🧊 Windows Executable

A compiled Windows setup file is available.

### 🔨 Build it yourself:

To build the `.exe` manually using PyInstaller:

```bash
pyinstaller InvestmentApp.spec
```

The output will be available in the `dist/` directory and includes all necessary assets.

---

## ✅ Completed Features

- Portfolio input with validation  
- Investment summary and projection  
- Theme switching via `.qss`  
- Real-time CAGR from Yahoo Finance  
- Error handling for invalid tickers  
- Interactive chart with zoom and pan  
- App icon integration  
- One-click `.exe` build with PyInstaller
- Unit testing with pytest

---

## 📌 Notes

- The Windows installer includes all dependencies — no Python required.
- Designed for educational/simulation purposes.
- Contributions and feedback are welcome!
