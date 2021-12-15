from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel
from game.GameState import GameStatus

class StatusWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.status_label = QLabel()

        layout = QGridLayout()
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def set_status(self, status: GameStatus):
        text = "Test"
        if status == GameStatus.TURN_PLAYER_0:
            text = "Player 1"
        elif status == GameStatus.TURN_PLAYER_1:
            text = "Player 2"
        self.status_label.setText(text)