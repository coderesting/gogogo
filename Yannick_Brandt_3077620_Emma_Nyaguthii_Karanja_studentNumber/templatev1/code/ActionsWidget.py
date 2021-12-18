from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QHBoxLayout

from BigButton import BigButton


class ActionsWidget(QWidget):
    reset = pyqtSignal()
    pass_stone = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.reset_button = BigButton("Reset")
        self.reset_button.clicked.connect(self.reset.emit)

        self.pass_button = BigButton("Pass")
        self.pass_button.clicked.connect(self.pass_stone.emit)

        layout = QHBoxLayout()
        layout.setSpacing(20)
        layout.addWidget(self.reset_button)
        layout.addWidget(self.pass_button)

        self.setLayout(layout)
        self.setMinimumWidth(300)
