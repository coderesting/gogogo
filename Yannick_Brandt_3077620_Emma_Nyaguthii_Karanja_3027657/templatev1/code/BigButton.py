from PyQt5.QtWidgets import QPushButton


class BigButton(QPushButton):
    """Shows a big button"""

    def __init__(self, title):
        super().__init__(title)
        self.setStyleSheet('font-size:16px; padding:10px')