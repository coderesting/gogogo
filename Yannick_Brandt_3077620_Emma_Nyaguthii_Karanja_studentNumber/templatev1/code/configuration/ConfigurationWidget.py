from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QGridLayout, QPushButton, QHBoxLayout

from configuration.GameConfiguration import GameConfiguration
from configuration.HandicapInput import HandicapInput


class ConfigurationWidget(QWidget):
    start_game = pyqtSignal(GameConfiguration)
    show_tutorial = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        welcome_label = QLabel("Welcome to GoGoGo")
        welcome_label.setStyleSheet("font-size: 20px")
        welcome_label.setAlignment(Qt.AlignCenter)

        black_stone = QLabel()
        black_stone.setPixmap(QPixmap('icons/blackStone.png').scaledToWidth(30))
        black_stone.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        white_stone = QLabel()
        white_stone.setPixmap(QPixmap('icons/whiteStone.png').scaledToWidth(30))
        white_stone.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        welcome_layout = QHBoxLayout()
        welcome_layout.addStretch()
        welcome_layout.addWidget(black_stone)
        welcome_layout.addWidget(welcome_label)
        welcome_layout.addWidget(white_stone)
        welcome_layout.addStretch()
        welcome_layout.setContentsMargins(20, 20, 20, 20)

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

        button_layout = QHBoxLayout()

        help_game_button = QPushButton("How to play")
        help_game_button.setStyleSheet("font-size: 16px; padding:15px")
        help_game_button.clicked.connect(self.show_tutorial.emit)
        button_layout.addWidget(help_game_button)

        start_game_button = QPushButton("Start Game")
        start_game_button.setStyleSheet("font-size: 16px; padding:15px")
        start_game_button.clicked.connect(self.trigger_game_start)
        button_layout.addWidget(start_game_button)

        layout = QGridLayout()
        layout.addLayout(welcome_layout, 0, 0, 1, 3)

        layout.addWidget(player_1_label, 1, 0)
        layout.addWidget(self.player_1_name_input, 2, 0)

        layout.addWidget(against_label, 2, 1)

        layout.addWidget(player_2_label, 1, 2)
        layout.addWidget(self.player_2_name_input, 2, 2)

        layout.addWidget(handicap_label, 3, 0, 1, 3)
        layout.addWidget(self.handicap_input, 4, 0, 1, 3)

        layout.addLayout(button_layout, 5, 0, 1, 3)

        layout.spacerItem()

        self.setLayout(layout)

    def trigger_game_start(self):
        conf = GameConfiguration(self.player_1_name_input.text(), self.player_2_name_input.text(),
                                 self.handicap_input.get_handicap())
        self.start_game.emit(conf)
