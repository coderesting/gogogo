from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QLabel

from ActionsWidget import ActionsWidget
from AnalyzeWidget import AnalyzeWidget
from BoardWidget import BoardWidget
from ConfigurationWidget import ConfigurationWidget
from Game import Game
from GameConfiguration import GameConfiguration
from GameState import GameStatus, is_end_status
from PlayerWidget import PlayerWidget
from ResultWidget import ResultWidget
from StatusWidget import StatusWidget


class GoApplication(QMainWindow):

    def __init__(self):
        super().__init__()

        self.game = Game()

        self.configuration_widget = ConfigurationWidget()
        self.status_widget = StatusWidget()
        self.boardWidget = BoardWidget()
        self.result_widget = ResultWidget()
        self.playerWidgets = [PlayerWidget('Tom', QColor('white'), parent=self),
                              PlayerWidget('Ellie', QColor('black'), parent=self)]
        self.actionsWidget = ActionsWidget()
        self.analyze_widget = AnalyzeWidget()

        self.connect_widgets()

        self.central_widget = QWidget()
        self.layout = QGridLayout()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.conf = GameConfiguration('Tom', 'Ellie', 0)

        self.configure_game()

        self.setWindowTitle('Go go go')
        self.setWindowIcon(QIcon('assets/appIcon.png'))
        self.show()

    def connect_widgets(self):
        self.configuration_widget.start_game.connect(self.start_new_game)

        self.boardWidget.clicked_field.connect(self.game.place_stone)

        self.game.invalid_move.connect(self.boardWidget.show_invalid_move)
        self.game.board_state_changed.connect(self.boardWidget.set_state)
        self.game.player_states_changed.connect(self.player_states_changed)
        self.game.game_status_changed.connect(self.game_status_changed)

        self.result_widget.new_game.connect(self.configure_game)
        self.result_widget.analyze.connect(self.analyze_game)

        self.analyze_widget.show_step.connect(self.game.rewind)
        self.analyze_widget.new_game.connect(self.configure_game)

    def game_status_changed(self, status: GameStatus):
        if is_end_status(status):
            self.game_ended()
        self.status_widget.set_status(status)

    def player_states_changed(self, states):
        self.playerWidgets[0].set_state(states[0])
        self.playerWidgets[1].set_state(states[1])

    def show_rules(self):
        self.clear_layout()
        self.layout.addWidget(QLabel("Rules"))

    def configure_game(self):
        self.clear_layout()
        self.layout.addWidget(self.configuration_widget, 0, 0)

    def start_new_game(self, conf: GameConfiguration):
        self.clear_layout()
        self.playerWidgets[0] = PlayerWidget(conf.names[0], QColor('black'))
        self.playerWidgets[1] = PlayerWidget(conf.names[1], QColor('black'))

        self.layout.addWidget(self.playerWidgets[0], 0, 0)
        self.layout.addWidget(self.status_widget, 0, 1)
        self.layout.addWidget(self.playerWidgets[1], 0, 2)
        self.layout.addWidget(self.boardWidget, 1, 1)
        self.layout.addWidget(self.actionsWidget, 2, 1)

        self.boardWidget.set_active(True)
        self.game.reset(conf.handicap)

    def game_ended(self):
        self.clear_layout()
        self.layout.addWidget(self.playerWidgets[0], 0, 0)
        self.layout.addWidget(self.status_widget, 0, 1)
        self.layout.addWidget(self.playerWidgets[1], 0, 2)
        self.layout.addWidget(self.boardWidget, 1, 1)
        self.layout.addWidget(self.result_widget, 1, 1)

        self.boardWidget.set_active(False)

    def analyze_game(self):
        self.clear_layout()
        self.layout.addWidget(self.playerWidgets[0], 0, 0)
        self.layout.addWidget(self.status_widget, 0, 1)
        self.layout.addWidget(self.playerWidgets[1], 0, 2)
        self.layout.addWidget(self.boardWidget, 1, 1)
        self.layout.addWidget(self.analyze_widget, 2, 1)

        self.boardWidget.set_active(True)
        self.analyze_widget.set_history_steps(len(self.game.history) - 1)

    def clear_layout(self):
        widgets = [self.configuration_widget, self.playerWidgets[0], self.playerWidgets[1], self.status_widget,
                   self.boardWidget, self.actionsWidget, self.analyze_widget, self.result_widget]
        for widget in widgets:
            self.layout.removeWidget(widget)
            widget.setParent(None)
