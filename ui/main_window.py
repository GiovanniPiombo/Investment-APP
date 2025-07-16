from PySide6.QtWidgets import QWidget, QVBoxLayout, QStackedLayout, QPushButton, QSpacerItem, QSizePolicy, QLineEdit, QLabel, QHBoxLayout, QScrollArea, QApplication
from ui.homepage import Homepage
from ui.portfolio import Portfolio
from ui.settings import Settings
from ui.advanced import Advanced
from core.finance import Finance
import os
import sys

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        base_path = project_root
    
    full_path = os.path.join(base_path, relative_path)
    
    if not os.path.exists(full_path):
        script_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)
        if os.path.exists(script_dir_path):
            return script_dir_path
    
    return full_path

class MainWindow(QWidget):
    def __init__(self):
        self.mode = "default"
        super().__init__()
        self.create_interface()
        self.controller()

    def create_interface(self):
        self.setWindowTitle("Investment APP")
        self.resize(1280,720)
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.title = QLabel("InvestmentAPP")
        self.main_layout.addWidget(self.title)
        self.title.setObjectName("main_title")

        self.horizontal_layout = QHBoxLayout()
        self.main_layout.addLayout(self.horizontal_layout)

        self.sidebar = QVBoxLayout()
        self.horizontal_layout.addLayout(self.sidebar)
        
        self.home_button = QPushButton("Home")
        self.portfolio_button = QPushButton("Portfolio")
        self.settings_button = QPushButton("Settings")
        self.sidebar.addWidget(self.home_button)
        self.sidebar.addWidget(self.portfolio_button)
        self.sidebar.addWidget(self.settings_button)
        self.sidebar.addStretch()

        self.pages = QStackedLayout()
        self.portfolio = Portfolio()
        self.portfolio_scroll = QScrollArea()
        self.portfolio_scroll.setWidget(self.portfolio)
        self.portfolio_scroll.setWidgetResizable(True)
        self.portfolio_scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.homepage = Homepage()
        self.settings = Settings()
        self.advanced = Advanced()
        self.pages.addWidget(self.homepage)                 
        self.pages.addWidget(self.portfolio_scroll)         
        self.pages.addWidget(self.settings)
        self.pages.addWidget(self.advanced)               
        self.horizontal_layout.addLayout(self.pages)

    def controller(self):
        self.home_button.clicked.connect(lambda: self.pages.setCurrentIndex(0))
        self.portfolio_button.clicked.connect(lambda: self.pages.setCurrentIndex(1))
        self.settings_button.clicked.connect(lambda: self.pages.setCurrentIndex(2))
        self.settings.mode_changed.connect(self.change_mode)
        self.settings.theme_changed.connect(self.apply_theme)
        self.portfolio.investment_saved.connect(self.sendupdate)
        self.advanced.investment_saved.connect(self.sendupdate)

    def change_mode(self, mode):
        if mode == "default":
            self.portfolio_button.clicked.connect(lambda: self.pages.setCurrentIndex(1))
        elif mode == "advanced":
            self.portfolio_button.clicked.connect(lambda: self.pages.setCurrentIndex(3))

    def sendupdate(self, investment):
        finance = Finance(investment)
        results = finance.get_results()
        years, capital = finance.get_annual_breakdown()
        self.homepage.update_investment(results, years, capital)

    def apply_theme(self, theme_name):
        try:
            qss_path = get_resource_path(f"assets/{theme_name}.qss")
            if os.path.exists(qss_path):
                with open(qss_path, "r") as file:
                    stylesheet = file.read()
                    app = QApplication.instance()
                    if app:
                        app.setStyleSheet(stylesheet)
                        if hasattr(self.homepage, 'chart') and self.homepage.chart is not None:
                            self.homepage.chart.change_theme(theme_name)
            else:
                print(f"Warning: QSS file not found at {qss_path}")
        except Exception as e:
            print(f"Error applying theme: {e}")
