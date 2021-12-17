from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from configuration.GameConfiguration import GameConfiguration
from configuration.HandicapInput import HandicapInput
from configuration.MainActions import MainActions
from configuration.PlayerNameInput import PlayerNameInput
from configuration.TimerInput import TimerInput
from configuration.WelcomeHeadline import WelcomeHeadline


class ConfigurationWidget(QWidget):
    start_game = pyqtSignal(GameConfiguration)
    show_tutorial = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        welcome_headline = WelcomeHeadline()

        self.player_name_input = PlayerNameInput()

        self.handicap_input = HandicapInput()

        self.timer_input = TimerInput()

        self.main_actions = MainActions()
        self.main_actions.show_tutorial.connect(self.show_tutorial.emit)
        self.main_actions.start_game.connect(self.trigger_game_start)
        self.player_name_input.error_state_changed.connect(self.main_actions.set_disabled)

        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.addStretch()
        layout.addWidget(welcome_headline)
        layout.addWidget(self.player_name_input)
        layout.addWidget(self.handicap_input)
        layout.addWidget(self.timer_input)
        layout.addWidget(self.main_actions)
        layout.addStretch()
        self.setMaximumWidth(600)
        self.setMinimumWidth(400)

        layout.spacerItem()

        self.setLayout(layout)

    def trigger_game_start(self):
        conf = GameConfiguration(self.player_name_input.get_player_names(), self.handicap_input.get_handicap(),
                                 self.timer_input.get_time_limit())
        self.start_game.emit(conf)
