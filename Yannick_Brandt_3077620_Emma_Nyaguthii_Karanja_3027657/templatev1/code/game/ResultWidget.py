from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QHBoxLayout

from BigButton import BigButton


class ResultWidget(QWidget):
    """Allows the user to analyze or start a new game after the current one ended

    :signal new_game(): Request to start a new game
    :signal analyze(): Request to show the analysis layout
    """
    new_game = pyqtSignal()
    analyze = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        analyze_button = BigButton("Analyze Game")
        analyze_button.clicked.connect(self.analyze.emit)

        # Add spaces to make buttons equal length for visual balance
        new_game_button = BigButton("  New Game  ")
        new_game_button.clicked.connect(self.new_game.emit)

        layout = QHBoxLayout()
        layout.setSpacing(40)
        layout.addStretch()
        layout.addWidget(analyze_button)
        layout.addWidget(new_game_button)
        layout.addStretch()
        self.setLayout(layout)
