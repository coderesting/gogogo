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

        self.start_game_button = QPushButton("Start Game")
        self.start_game_button.setStyleSheet("font-size: 16px; padding:10px")
        self.start_game_button.clicked.connect(self.start_game.emit)
        self.start_game_button.setDefault(True)
        button_layout.addWidget(self.start_game_button, 7)
        button_layout.setContentsMargins(5, 15, 5, 0)

        self.setLayout(button_layout)

    def set_disabled(self, disabled: bool):
        self.start_game_button.setDisabled(disabled)
