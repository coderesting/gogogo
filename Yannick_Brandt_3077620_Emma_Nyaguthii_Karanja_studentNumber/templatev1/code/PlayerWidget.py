from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout

from PlayerState import PlayerState


class PlayerWidget(QWidget):
    def __init__(self, name: str, color: QColor, parent=None):
        super().__init__(parent)
        self.label = QLabel("leel")
        layout = QHBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

    def set_state(self, state: PlayerState):
        self.label.setText("captures:" + str(state.captured_stones) + "\n territory:" + str(state.territory))
