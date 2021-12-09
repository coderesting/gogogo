from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QGridLayout, QPushButton

from GameConfiguration import GameConfiguration
from HandicapInput import HandicapInput


class ConfigurationWidget(QWidget):
    start_game = pyqtSignal(GameConfiguration)

    def __init__(self, parent=None):
        super().__init__(parent)

        welcome_label = QLabel("Welcome to GoGoGo")
        welcome_label.setAlignment(Qt.AlignCenter)

        player_1_label = QLabel("Player 1 (black)")
        self.player_1_name_input = QLineEdit()
        self.player_1_name_input.setPlaceholderText("name")

        against_label = QLabel("-")

        player_2_label = QLabel("Player 2 (white)")
        self.player_2_name_input = QLineEdit()
        self.player_2_name_input.setPlaceholderText("name")

        handicap_label = QLabel("Handicap (extra points for white)")
        handicap_label.setAlignment(Qt.AlignCenter)
        self.handicap_input = HandicapInput()

        start_game_button = QPushButton("Start Game")
        start_game_button.clicked.connect(self.trigger_game_start)

        layout = QGridLayout()
        layout.addWidget(welcome_label, 0, 0, 1, 3)

        layout.addWidget(player_1_label, 1, 0)
        layout.addWidget(self.player_1_name_input, 2, 0)

        layout.addWidget(against_label, 2, 1)

        layout.addWidget(player_2_label, 1, 2)
        layout.addWidget(self.player_2_name_input, 2, 2)

        layout.addWidget(handicap_label, 3, 0, 1, 3)
        layout.addWidget(self.handicap_input, 4, 0, 1, 3)

        layout.addWidget(start_game_button, 5, 0, 1, 3)

        self.setLayout(layout)

    def trigger_game_start(self):
        conf = GameConfiguration(self.player_1_name_input.text(), self.player_2_name_input.text(),
                                 self.handicap_input.get_handicap())
        self.start_game.emit(conf)
