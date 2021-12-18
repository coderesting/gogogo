from time import strftime, gmtime

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QWidget, QLabel

from game.player.PlayerState import PlayerState


class PlayerWidget(QWidget):
    def __init__(self, name: str, stone: QPixmap, parent=None):
        super().__init__(parent)
        self.captures = QLabel()
        self.time = QLabel()
        self.territory = QLabel()

        layout = QGridLayout()
        layout.addWidget(self.captures)
        layout.addWidget(self.time)
        layout.addWidget(self.territory)

        self.setLayout(layout)

    def set_state(self, state: PlayerState):
        self.captures.setText("Captures: " + str(state.captured_stones))
        self.time.setText("Remaining time " + strftime("%M:%S", gmtime(state.remaining_time)) + " mins")
