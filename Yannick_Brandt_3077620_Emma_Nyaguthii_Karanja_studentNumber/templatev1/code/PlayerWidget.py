from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget

from PlayerState import PlayerState


class PlayerWidget(QWidget):
    def __init__(self, name: str, color: QColor, parent=None):
        super().__init__(parent)

    def set_state(self, state: PlayerState): pass
