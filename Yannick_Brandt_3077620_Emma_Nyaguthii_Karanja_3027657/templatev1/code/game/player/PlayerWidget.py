from time import strftime, gmtime

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGroupBox
from PyQt5.QtWidgets import QLabel

from game.player.PlayerState import PlayerState


class PlayerWidget(QGroupBox):
    def __init__(self, name: str, stone_pixmap: QPixmap, parent=None):
        super().__init__(parent)
        self.name = name

        self.stone_label = QLabel()
        self.stone_label.setPixmap(stone_pixmap.scaledToWidth(30, Qt.SmoothTransformation))

        self.player_name = QLabel()
        self.player_name.setStyleSheet("font-size:14px")

        self.captured_stones = QLabel()
        self.captured_stones.setStyleSheet("font-size:12px")

        self.own_stones = QLabel()
        self.own_stones.setStyleSheet("font-size:12px")

        self.territory = QLabel()
        self.territory.setStyleSheet("font-size:12px")

        self.score = QLabel()
        self.score.setStyleSheet("font-size:12px")

        self.time = QLabel()
        self.time.setStyleSheet("font-size:12px")

        headline_layout = QHBoxLayout()
        headline_layout.setSpacing(10)
        headline_layout.setAlignment(Qt.AlignLeft)
        headline_layout.addWidget(self.stone_label)
        headline_layout.addWidget(self.player_name)

        player_layout = QVBoxLayout()
        player_layout.setSpacing(20)
        player_layout.addLayout(headline_layout)
        player_layout.addWidget(self.own_stones)
        player_layout.addWidget(self.captured_stones)
        player_layout.addWidget(self.territory)
        player_layout.addWidget(self.score)
        player_layout.addWidget(self.time)

        player_layout.addStretch()

        self.setLayout(player_layout)
        self.setStyleSheet('QGroupBox{background:white; padding:5px 2px}')
        self.setMinimumWidth(200)

    def set_state(self, state: PlayerState):
        self.player_name.setText(self.name)

        self.captured_stones.setText("Captured stones: " + str(state.captured_stones))

        self.own_stones.setText("Own stones: " + str(state.own_stones))

        self.territory.setText("Territory: " + str(state.territory))

        self.score.setText("Score: " + str(state.captured_stones + state.own_stones + state.territory))

        if state.remaining_time is not None:
            self.time.show()
            self.time.setText("Remaining time " + strftime("%M:%S", gmtime(state.remaining_time)))
        else:
            self.time.hide()
