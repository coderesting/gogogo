from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QLabel

from ActionsWidget import ActionsWidget
from AnalyzeWidget import AnalyzeWidget
from BoardWidget import BoardWidget
from Game import Game
from GameState import GameState
from PlayerWidget import PlayerWidget
from ResultWidget import ResultWidget
from StatusWidget import StatusWidget


class GoApplication(QMainWindow):

    def __init__(self):
        super().__init__()

        self.game = Game()

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

        self.game_ended()

        self.setWindowTitle('Go go go')
        self.setWindowIcon(QIcon('assets/appIcon.png'))
        self.show()

    def connect_widgets(self):
        self.result_widget.new_game.connect(self.configure_game)
        self.result_widget.analyze.connect(self.analyze_game)

        self.boardWidget.clicked_field.connect(self.game.place_stone)

        self.game.invalid_move.connect(self.boardWidget.show_invalid_move)
        self.game.board_state_changed.connect(self.boardWidget.set_state)
        self.game.player_state_changed.connect(lambda idx, state: self.playerWidgets[idx].set_state(state))
        self.game.game_state_changed.connect(self.game_state_changed)

    def game_state_changed(self, state: GameState):
        if state == GameState.END_RESIGN or state == GameState.END_NO_MOVES or state == GameState.END_TWO_PASSES:
            self.game_ended()
        self.status_widget.set_status(state)

    def show_rules(self):
        self.clear_layout()
        self.layout.addWidget(QLabel("Rules"))

    def configure_game(self):
        self.clear_layout()
        self.layout.addWidget(QLabel("Configure"), 0, 0)

    def start_game(self):
        self.clear_layout()
        self.layout.addWidget(self.playerWidgets[0], 0, 0)
        self.layout.addWidget(self.status_widget, 0, 1)
        self.layout.addWidget(self.playerWidgets[1], 0, 2)
        self.layout.addWidget(self.boardWidget, 1, 1)
        self.layout.addWidget(self.actionsWidget, 2, 1)

        self.boardWidget.set_active(True)

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

    def clear_layout(self):
        self.layout.removeWidget(self.playerWidgets[0])
        self.layout.removeWidget(self.status_widget)
        self.layout.removeWidget(self.playerWidgets[1])
        self.layout.removeWidget(self.boardWidget)
        self.layout.removeWidget(self.actionsWidget)
