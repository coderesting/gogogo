from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout

from game.GameState import GameStatus, is_end_status
from game.GameState import WinnerStatus


class StatusWidget(QWidget):
    def __init__(self, player_names, parent=None):
        super().__init__(parent)
        self.player_names = player_names

        self.status_label = QLabel()
        self.status_label.setStyleSheet('font-size:16px')
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)

        layout = QHBoxLayout()
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def set_status(self, game_status: GameStatus, winner_status: WinnerStatus):
        text = "Test"
        if is_end_status(game_status):
            if winner_status == WinnerStatus.PLAYER_0:
                text = self.player_names[0] + ' won'
            elif winner_status == WinnerStatus.PLAYER_1:
                text = self.player_names[1] + ' won'
            elif winner_status == WinnerStatus.DRAW:
                text = 'Draw'

            if game_status == GameStatus.END_TIMEOUT:
                text += '\n(Timeout)'
            elif game_status == GameStatus.END_NO_MOVES:
                text += '\n(No moves left)'
            elif game_status == GameStatus.END_TWO_PASSES:
                text += '\n(Two passes)'
        else:
            if game_status == GameStatus.TURN_PLAYER_0:
                text = self.player_names[0] + "'s turn"
            elif game_status == GameStatus.TURN_PLAYER_1:
                text = self.player_names[1] + "'s turn"
            elif game_status == GameStatus.ANALYSIS:
                text = "Analysis"

        self.status_label.setText(text)
