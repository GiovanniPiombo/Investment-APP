from PySide6.QtWidgets import QWidget, QVBoxLayout, QStackedLayout, QPushButton, QLabel, QHBoxLayout, QScrollArea, QApplication
from PySide6.QtCore import QSize
from ui.homepage import Homepage
from ui.portfolio import Portfolio
from ui.settings import Settings
from ui.advanced import Advanced
from core.finance import Finance
import os
import sys

def get_resource_path(relative_path):
    """Get the absolute path to a resource, works for both development and PyInstaller"""
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
    """Main window for the Investment Application"""
    
    # Constants
    WINDOW_TITLE = "Investment APP"
    DEFAULT_SIZE = QSize(1280, 720)
    
    # Page indices
    PAGE_HOME = 0
    PAGE_PORTFOLIO = 1
    PAGE_SETTINGS = 2
    PAGE_ADVANCED = 3
    
    # Modes
    MODE_DEFAULT = "default"
    MODE_ADVANCED = "advanced"

    def __init__(self):
        super().__init__()
        self.mode = self.MODE_DEFAULT
        self._init_ui_components()
        self._setup_ui()
        self._connect_signals()

    def _init_ui_components(self):
        """Initialize UI components"""
        # Main layout
        self.main_layout = QVBoxLayout()
        
        # Pages and widgets
        self.homepage = Homepage()
        self.portfolio = Portfolio()
        self.settings = Settings()
        self.advanced = Advanced()
        
        # Navigation buttons
        self.home_button = QPushButton("Home")
        self.portfolio_button = QPushButton("Portfolio")
        self.settings_button = QPushButton("Settings")

    def _setup_ui(self):
        """Setup the main user interface"""
        self._configure_window()
        self._create_title()
        self._create_main_layout()
        self._create_sidebar()
        self._create_content_area()

    def _configure_window(self):
        """Configure main window properties"""
        self.setWindowTitle(self.WINDOW_TITLE)
        self.resize(self.DEFAULT_SIZE)
        self.setLayout(self.main_layout)

    def _create_title(self):
        """Create and setup the main title"""
        self.title = QLabel("InvestmentAPP")
        self.title.setObjectName("main_title")
        self.main_layout.addWidget(self.title)

    def _create_main_layout(self):
        """Create the horizontal layout that contains sidebar and content"""
        self.horizontal_layout = QHBoxLayout()
        self.main_layout.addLayout(self.horizontal_layout)

    def _create_sidebar(self):
        """Create and setup the navigation sidebar"""
        self.sidebar = QVBoxLayout()
        
        # Add navigation buttons
        navigation_buttons = [
            self.home_button,
            self.portfolio_button,
            self.settings_button
        ]
        
        for button in navigation_buttons:
            self.sidebar.addWidget(button)
        
        self.sidebar.addStretch()
        self.horizontal_layout.addLayout(self.sidebar)

    def _create_content_area(self):
        """Create and setup the main content area with pages"""
        self.pages = QStackedLayout()
        
        # Setup portfolio with scroll area
        portfolio_scroll = self._create_scrollable_widget(self.portfolio)
        
        # Add pages in order
        pages_to_add = [
            self.homepage,      # PAGE_HOME = 0
            portfolio_scroll,   # PAGE_PORTFOLIO = 1
            self.settings,      # PAGE_SETTINGS = 2
            self.advanced       # PAGE_ADVANCED = 3
        ]
        
        for page in pages_to_add:
            self.pages.addWidget(page)
        
        self.horizontal_layout.addLayout(self.pages)

    def _create_scrollable_widget(self, widget):
        """Create a scrollable container for a widget"""
        scroll_area = QScrollArea()
        scroll_area.setWidget(widget)
        scroll_area.setWidgetResizable(True)
        return scroll_area

    def _connect_signals(self):
        """Connect all signals to their respective slots"""
        self._connect_navigation_signals()
        self._connect_settings_signals()
        self._connect_investment_signals()

    def _connect_navigation_signals(self):
        """Connect navigation button signals"""
        self.home_button.clicked.connect(lambda: self._navigate_to_page(self.PAGE_HOME))
        self.portfolio_button.clicked.connect(self._handle_portfolio_navigation)
        self.settings_button.clicked.connect(lambda: self._navigate_to_page(self.PAGE_SETTINGS))

    def _connect_settings_signals(self):
        """Connect settings-related signals"""
        self.settings.mode_changed.connect(self._change_mode)
        self.settings.theme_changed.connect(self._apply_theme)

    def _connect_investment_signals(self):
        """Connect investment update signals"""
        self.portfolio.investment_saved.connect(self._handle_investment_update)
        self.advanced.investment_saved.connect(self._handle_investment_update)

    def _navigate_to_page(self, page_index):
        """Navigate to a specific page"""
        self.pages.setCurrentIndex(page_index)

    def _handle_portfolio_navigation(self):
        """Handle portfolio button click based on current mode"""
        if self.mode == self.MODE_DEFAULT:
            self._navigate_to_page(self.PAGE_PORTFOLIO)
        elif self.mode == self.MODE_ADVANCED:
            self._navigate_to_page(self.PAGE_ADVANCED)

    def _change_mode(self, mode):
        """Change the application mode"""
        self.mode = mode
        # Navigation is now handled by _handle_portfolio_navigation method
        # No need to reconnect signals

    def _handle_investment_update(self, investment):
        """Handle investment data updates"""
        try:
            finance = Finance(investment)
            results = finance.get_results()
            years, capital = finance.get_annual_breakdown()
            self.homepage.update_investment(results, years, capital)
        except Exception as e:
            print(f"Error updating investment: {e}")

    def _apply_theme(self, theme_name):
        """Apply the selected theme to the application"""
        try:
            qss_path = get_resource_path(f"assets/{theme_name}.qss")
            
            if not os.path.exists(qss_path):
                print(f"Warning: QSS file not found at {qss_path}")
                return
            
            with open(qss_path, "r", encoding="utf-8") as file:
                stylesheet = file.read()
            
            app = QApplication.instance()
            if app:
                app.setStyleSheet(stylesheet)
                self._update_chart_theme(theme_name)
                
        except Exception as e:
            print(f"Error applying theme: {e}")

    def _update_chart_theme(self, theme_name):
        """Update chart theme if available"""
        if (hasattr(self.homepage, 'chart') and 
            self.homepage.chart is not None and
            hasattr(self.homepage.chart, 'change_theme')):
            self.homepage.chart.change_theme(theme_name)