from PyQt5.QtWidgets import QWidget

from GameState import GameState


class StatusWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_status(self, game_state: GameState):
        print(game_state)
