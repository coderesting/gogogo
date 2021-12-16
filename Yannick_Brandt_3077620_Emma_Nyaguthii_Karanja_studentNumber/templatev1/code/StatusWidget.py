from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel

from game.GameState import GameStatus
from game.GameState import WinnerStatus


class StatusWidget(QWidget):
    def __init__(self, player_names, parent=None):
        super().__init__(parent)
        self.status_label = QLabel()

        layout = QGridLayout()
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def set_status(self, game_status: GameStatus, winner_status: WinnerStatus):
        text = "Test"
        if game_status == GameStatus.TURN_PLAYER_0:
            text = "Player 1"
        elif game_status == GameStatus.TURN_PLAYER_1:
            text = "Player 2"
        self.status_label.setText(text)
