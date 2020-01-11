from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QStatusBar


class Statusbar(QStatusBar):
    def __init__(self):
        super().__init__()
        self.init_elements()

    def init_elements(self):
        self.addWidget(QLabel("Element1"))
        self.addWidget(QLabel("Element2"))