from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QHBoxLayout

from BigButton import BigButton


class ActionsWidget(QWidget):
    restart = pyqtSignal()
    pass_stone = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.restart_button = BigButton("Restart")
        self.restart_button.clicked.connect(self.restart.emit)

        self.pass_button = BigButton("Pass")
        self.pass_button.clicked.connect(self.pass_stone.emit)

        layout = QHBoxLayout()
        layout.setSpacing(20)
        layout.addWidget(self.restart_button)
        layout.addWidget(self.pass_button)

        self.setLayout(layout)
        self.setMinimumWidth(300)
