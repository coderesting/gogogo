from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton


class MainActions(QWidget):
    show_tutorial = pyqtSignal()
    start_game = pyqtSignal()

    def __init__(self):
        super().__init__()

        button_layout = QHBoxLayout()

        tutorial_button = QPushButton("How to play")
        tutorial_button.setStyleSheet("font-size: 16px; padding:10px")
        tutorial_button.clicked.connect(self.show_tutorial.emit)
        button_layout.addWidget(tutorial_button, 0)

        start_game_button = QPushButton("Start Game")
        start_game_button.setStyleSheet("font-size: 16px; padding:10px")
        start_game_button.clicked.connect(self.start_game.emit)
        start_game_button.setDefault(True)
        button_layout.addWidget(start_game_button, 7)
        button_layout.setContentsMargins(5, 15, 5, 0)

        self.setLayout(button_layout)

    def get_handicap(self):
        return self.handicap_group.checkedButton().data
