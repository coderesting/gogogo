from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLayout

from Window import Window
from configuration.GameConfiguration import GameConfiguration
from configuration.MainActions import MainActions
from configuration.WelcomeHeadline import WelcomeHeadline
from configuration.inputs.HandicapInput import HandicapInput
from configuration.inputs.PlayerNameInput import PlayerNameInput
from configuration.inputs.TimerInput import TimerInput


class ConfigurationWindow(Window):
    start_game = pyqtSignal(GameConfiguration)

    def __init__(self):
        super().__init__()
        welcome_headline = WelcomeHeadline()

        self.player_name_input = PlayerNameInput()

        self.handicap_input = HandicapInput()

        self.timer_input = TimerInput()

        self.main_actions = MainActions()
        self.main_actions.show_tutorial.connect(self.show_tutorial)
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

        self.central_widget = QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

        self.central_widget.setMinimumWidth(400)

        self.layout().setSizeConstraint(QLayout.SetFixedSize)

    def trigger_game_start(self):
        conf = GameConfiguration(self.player_name_input.get_player_names(), self.handicap_input.get_handicap(),
                                 self.timer_input.get_time_limit())
        self.start_game.emit(conf)
