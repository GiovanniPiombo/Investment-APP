# 💼 Investment App

**Investment App** is a desktop application built with **PySide6** that helps users simulate and track the growth of their investments over time. The app features a clean and intuitive interface, with modular pages for portfolio input, settings, and a homepage summary.

---

## 🚀 Features

- 📊 **Portfolio Input**  
  Enter your initial deposit, interest rate, contribution frequency, and other key parameters.

- 🧠 **Advanced Ticker-Based Simulation**  
  Input multiple **stock tickers** (e.g., AAPL, TSLA) and calculate their **historical CAGR** based on real market data:
  - Automatically fetches data from **Yahoo Finance**
  - Computes average annual return (CAGR) from 2020 to 2025
  - Supports weighted average across multiple tickers

- 🏠 **Homepage Summary**  
  Get a detailed breakdown of your investment projection and total returns.

- 📈 **Interactive Growth Chart**  
  Visual comparison between:
  - Compounded investment growth  
  - Total amount invested (linear)  
  - Theme-aware chart styling (light/dark)

- 🎚️ **Chart Controls**  
  - Mouse wheel: Zoom  
  - Click + drag: Pan  
  - Double-click: Reset view  
  - Rubber-band selection: Zoom to area

- ⚙️ **Theme Settings**  
  Easily switch between light and dark modes using `.qss` stylesheets.

- 🧩 **Modular Architecture**  
  Organized by components with clear signal-slot communication.

- 🖼️ **Custom App Icon**  
  Includes a personalized app icon (`icon.ico`) for a polished desktop experience.

- 💾 **Windows Setup (.exe)**  
  The app can be installed via a standalone Windows setup file — no Python installation required.

---

## 🧩 Project Structure

```
project/
├── assets/
│   ├── white.qss               # Stylesheet for light theme
│   ├── dark.qss                # Stylesheet for dark theme
│   └── icon.ico                # Custom app icon
├── core/
│   ├── ticker_analyzer.py      # Ticker CAGR
│   └── finance.py              # Core financial logic
├── ui/
│   ├── chart.py                # Chart Settings
│   ├── homepage.py             # Homepage summary page
│   ├── main_window.py          # Main application window
│   ├── portfolio.py            # Portfolio input form
│   ├── advanced.py             # Advanced page with multi-ticker input
│   ├── investment.py           # Individual investment input widget
│   └── settings.py             # Theme and app settings
├── main.py                     # App entry point
├── README.md                   # This file
├── requirements.txt            # Requirements
└── InvestmentApp.spec          # PyInstaller spec file for building .exe
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

3️⃣ Run the application:

```bash
python main.py
```

---

## 🧊 Windows Executable (Setup)

A compiled Windows setup file is available for installation.

### 🔨 Build it yourself (optional):

If you want to build the `.exe` yourself, use:

```bash
pyinstaller InvestmentApp.spec
```

This will generate a distributable .exe file in the dist/ directory.

The setup includes the icon and all required assets.

## ✅ Completed

- Portfolio input form with validation  
- Theme switching using `.qss` stylesheets  
- Investment summary display  
- Signal-slot communication between components  
- Interactive investment growth chart with zoom/pan controls
- App icon integration  
- PyInstaller `.exe` build and Windows setup
- Advanced investment page with real-time ticker analysis (CAGR)

---

## 📝 TODO

- [ ] **Improve error handling in TickerAnalyzer**  
  Gracefully handle invalid or unavailable tickers with user-friendly feedback.

- [ ] **Add unit testing with pytest**  
  Introduce automated tests for financial logic and ticker analysis using `pytest`.

## 📌 Notes

- The Windows installer requires no Python installation.
- Setup was created with PyInstaller and includes the custom icon.
- This app is designed for educational and simulation purposes only.  
- Contributions and feedback are welcome!
