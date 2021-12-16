from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout


class ResultWidget(QWidget):
    new_game = pyqtSignal()
    analyze = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout()
        layout.setSpacing(40)
        layout.addStretch()
        layout.setAlignment(Qt.AlignLeft)

        analyze_button = QPushButton("Analyze Game")
        analyze_button.setStyleSheet('font-size: 14px; padding:10px')
        analyze_button.clicked.connect(self.analyze.emit)
        layout.addWidget(analyze_button)

        new_game_button = QPushButton("  New Game  ")
        new_game_button.clicked.connect(self.new_game.emit)
        new_game_button.setStyleSheet('font-size: 14px; padding:10px')
        layout.addWidget(new_game_button)
        layout.addStretch()

        self.setLayout(layout)
