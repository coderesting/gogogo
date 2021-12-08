from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout


class ResultWidget(QWidget):
    new_game = pyqtSignal()
    analyze = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout()
        layout.addStretch()

        analyze_button = QPushButton("Analyze Game")
        analyze_button.clicked.connect(self.analyze.emit)
        layout.addWidget(analyze_button)

        layout.addStretch()

        new_game_button = QPushButton("New Game")
        new_game_button.clicked.connect(self.new_game.emit)
        layout.addWidget(new_game_button)
        layout.addStretch()

        self.setLayout(layout)
