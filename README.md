# 💼 Investment App

**Investment App** is a desktop application built with **PySide6** that helps users simulate and track the growth of their investments over time. The app features a clean and intuitive interface, with modular pages for portfolio input, settings, and a homepage summary.

---

## 🚀 Features

- 📊 **Portfolio Input**  
  Enter initial deposit, interest rate, contribution frequency, and other parameters.

- 🏠 **Homepage Summary**  
  View detailed information about your investments and growth projections.

- 📈 **Interactive Growth Chart**  
  Visualize investment performance with zoom/pan functionality and comparison between:  
  - Investment value (compounded growth)  
  - Total invested amount (straight-line)  
  - Theme-adaptive colors (dark/light mode)

- 🎚️ **Chart Controls**  
  - Mouse wheel: Zoom in/out  
  - Click + drag: Pan through chart  
  - Double-click: Reset view  
  - Rubber-band selection: Area zoom

- ⚙️ **Theme Settings**  
  Switch between light and dark themes using `.qss` stylesheets.

- 📁 **Modular UI**  
  Built with reusable components using Qt layouts and signal-slot communication.

---

## 🧩 Project Structure

```
project/
├── assets/
│   ├── white.qss               # Stylesheet for light theme
│   └── dark.qss                # Stylesheet for dark theme
├── core/
│   └── finance.py              # Core financial logic
├── ui/
│   ├── chart.py                # Chart Settings
│   ├── homepage.py             # Homepage summary page
│   ├── main_window.py          # Main application window
│   ├── portfolio.py            # Portfolio input form
│   └── settings.py             # Theme and app settings
├── main.py                     # App entry point
├── README.md                   # This file
└── requirements.txt            # Requirements
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

## ✅ Completed

- Portfolio input form with validation  
- Theme switching using `.qss` stylesheets  
- Investment summary display  
- Signal-slot communication between components  
- Interactive investment growth chart with zoom/pan controls  

---

## 🔧 TODO

- 🧊 **Executable Build**  
  Packaging the app into a `.exe` for Windows using **PyInstaller**

---

## 📌 Notes

- This app is designed for educational and simulation purposes only.  
- Contributions and feedback are welcome!
