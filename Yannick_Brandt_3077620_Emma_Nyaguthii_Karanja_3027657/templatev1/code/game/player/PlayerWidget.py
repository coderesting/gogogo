from time import strftime, gmtime

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGroupBox, QCheckBox
from PyQt5.QtWidgets import QLabel

from game.player.PlayerState import PlayerState


class PlayerWidget(QGroupBox):
    def __init__(self, name: str, stone_pixmap: QPixmap, stone_active_pixmap: QPixmap, parent=None):
        super().__init__(parent)
        self.stone_pixmap = stone_pixmap.scaledToWidth(30, Qt.SmoothTransformation)
        self.stone_active_pixmap = stone_active_pixmap.scaledToWidth(30, Qt.SmoothTransformation)

        self.stone_label = QLabel()
        self.stone_label.setPixmap(stone_pixmap.scaledToWidth(30, Qt.SmoothTransformation))
        self.player_name = QLabel(name)

        headline_layout = QHBoxLayout()
        headline_layout.setSpacing(10)
        headline_layout.setAlignment(Qt.AlignLeft)
        headline_layout.addWidget(self.stone_label)
        headline_layout.addWidget(self.player_name)

        self.captured_stones = QLabel()
        self.own_stones = QLabel()
        self.territory = QLabel()
        self.score = QLabel()
        self.time = QLabel()

        self.hide_time_label = QLabel("Hide time: ")
        self.hide_time_checkbox = QCheckBox()
        self.hide_time_checkbox.stateChanged.connect(lambda val: self.time.hide() if val else self.time.show())

        hide_time_layout = QHBoxLayout()
        hide_time_layout.setAlignment(Qt.AlignLeft)
        hide_time_layout.addWidget(self.hide_time_label)
        hide_time_layout.addWidget(self.hide_time_checkbox)

        player_layout = QVBoxLayout()
        player_layout.setSpacing(20)
        player_layout.addLayout(headline_layout)
        player_layout.addWidget(self.own_stones)
        player_layout.addWidget(self.captured_stones)
        player_layout.addWidget(self.territory)
        player_layout.addWidget(self.score)
        player_layout.addWidget(self.time)
        player_layout.addLayout(hide_time_layout)

        player_layout.addStretch()

        self.setLayout(player_layout)
        self.setStyleSheet('QGroupBox{background:white; padding:10px} QLabel{font-size:12px}')
        self.setMinimumWidth(200)

    def set_state(self, state: PlayerState):

        self.stone_label.setPixmap(self.stone_active_pixmap if state.is_playing else self.stone_pixmap)

        self.player_name.setStyleSheet(
            'font-size:14px; text-decoration: ' + ('underline' if state.is_playing else 'none'))

        self.captured_stones.setText("Captured stones: " + str(state.captured_stones))

        self.own_stones.setText("Own stones: " + str(state.own_stones))

        self.territory.setText("Territory: " + str(state.territory))

        self.score.setText("<b>Score: " + str(state.captured_stones + state.own_stones + state.territory) + '</b>')

        if state.remaining_time is not None and self.hide_time_checkbox.checkState() == 0:
            self.time.show()
            self.time.setText("Remaining time: " + strftime("%M:%S", gmtime(state.remaining_time)))
        else:
            self.time.hide()

        if state.remaining_time is not None:
            self.hide_time_checkbox.show()
            self.hide_time_label.show()
        else:
            self.hide_time_checkbox.hide()
            self.hide_time_label.hide()
