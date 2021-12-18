from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QPushButton


class BigButton(QPushButton):
    """Shows a big button"""

    def __init__(self, title):
        super().__init__(title)
        self.setFont(QFont('Arial', 15))
