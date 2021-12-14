from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton

class ActionsWidget(QWidget):
    reset = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QGridLayout()

        self.reset_button = QPushButton("Reset", self)
        self.reset_button.clicked.connect(self.reset.emit)
        layout.addWidget(self.reset_button, 0, 0)

        self.setLayout(layout)

