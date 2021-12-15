from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QGridLayout
from time import strftime, gmtime

from player.PlayerState import PlayerState


class PlayerWidget(QWidget):
    def __init__(self, name: str, color: QColor, parent=None):
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
        self.captures.setText("Captures: "+str(state.captured_stones))
        self.time.setText("Remaining time " + strftime("%M:%S", gmtime(state.remaining_time)) + " mins")
