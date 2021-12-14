from PyQt5.QtWidgets import QWidget, QGridLayout
from game.GameState import GameStatus

class StatusWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QGridLayout()

    def set_status(self, status: GameStatus):
        print(status)
