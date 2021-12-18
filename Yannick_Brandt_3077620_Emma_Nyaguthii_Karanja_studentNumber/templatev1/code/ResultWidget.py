from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout

from BigButton import BigButton


class ResultWidget(QWidget):
    new_game = pyqtSignal()
    analyze = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout()
        layout.setSpacing(40)
        layout.addStretch()
        layout.setAlignment(Qt.AlignLeft)

        analyze_button = BigButton("Analyze Game")
        analyze_button.clicked.connect(self.analyze.emit)
        layout.addWidget(analyze_button)

        new_game_button = BigButton("  New Game  ")
        new_game_button.clicked.connect(self.new_game.emit)
        layout.addWidget(new_game_button)
        layout.addStretch()

        self.setLayout(layout)
