from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLayout

from Window import Window
from configuration.GameConfiguration import GameConfiguration
from configuration.WelcomeHeadline import WelcomeHeadline
from configuration.inputs.ActionButtons import ActionButtons
from configuration.inputs.HandicapInput import HandicapInput
from configuration.inputs.PlayerNameInput import PlayerNameInput
from configuration.inputs.TimerInput import TimerInput


class ConfigurationWindow(Window):
    """Shows a window to configure the game of go

    :signal start_game(GameConfiguration): Request to start the game with the provided configuration
    """
    start_game = pyqtSignal(GameConfiguration)

    def __init__(self):
        super().__init__()
        welcome_headline = WelcomeHeadline()
        self.player_name_input = PlayerNameInput()
        self.handicap_input = HandicapInput()
        self.timer_input = TimerInput()

        self.action_buttons = ActionButtons()
        self.action_buttons.show_tutorial.connect(self.show_tutorial)
        self.action_buttons.start_game.connect(self.trigger_game_start)
        self.player_name_input.error_state_changed.connect(self.action_buttons.set_disabled)

        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.addStretch()
        layout.addWidget(welcome_headline)
        layout.addWidget(self.player_name_input)
        layout.addWidget(self.handicap_input)
        layout.addWidget(self.timer_input)
        layout.addWidget(self.action_buttons)
        layout.addStretch()

        self.central_widget = QWidget()
        self.central_widget.setContentsMargins(10, 10, 10, 10)
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

        self.central_widget.setMinimumWidth(400)
        # Prevent resizing
        self.layout().setSizeConstraint(QLayout.SetFixedSize)

    def trigger_game_start(self):
        conf = GameConfiguration(self.player_name_input.get_player_names(), self.handicap_input.get_handicap(),
                                 self.timer_input.get_time_limit())
        self.start_game.emit(conf)
