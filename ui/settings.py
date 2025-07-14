from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy, QComboBox, QPushButton
from PySide6.QtCore import Qt, Signal

class Settings(QWidget):
    theme_changed = Signal(str)
    mode_changed = Signal(str)

    def __init__(self):
        super().__init__()
        self.create_settings_page()

    def create_settings_page(self):
        self.settings_layout = QVBoxLayout()
        self.settings_layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.settings_layout)
        self.title = QLabel("Settings")
        self.title.setObjectName("settings_title")
        self.settings_layout.addWidget(self.title)
        self.setLayout(self.settings_layout)
        self.settings_layout.addWidget(QLabel("Theme"))
        self.theme_selector = QComboBox()
        self.theme_selector.addItems(["White","Dark"])
        self.settings_layout.addWidget(self.theme_selector)
        self.settings_layout.addWidget(QLabel("Advanced Mode"))
        self.mode_selector = QComboBox()
        self.mode_selector.addItems(["Default","Advanced"])
        self.settings_layout.addWidget(self.mode_selector)
        self.save_button = QPushButton("Save")
        self.settings_layout.addWidget(self.save_button)
        self.save_button.clicked.connect(lambda: self.theme_changed.emit(self.theme_selector.currentText().lower()))
        self.save_button.clicked.connect(lambda: self.mode_changed.emit(self.mode_selector.currentText().lower()))
