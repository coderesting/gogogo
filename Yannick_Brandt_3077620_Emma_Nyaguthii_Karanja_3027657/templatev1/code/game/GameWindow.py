from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QGridLayout

from Window import Window
from board.BoardWidget import BoardWidget
from configuration.GameConfiguration import GameConfiguration
from game.ActionsWidget import ActionsWidget
from game.AnalyzeWidget import AnalyzeWidget
from game.Game import Game
from game.GameState import GameStatus, is_end_status
from game.ResultWidget import ResultWidget
from game.StatusWidget import StatusWidget
from game.player.PlayerWidget import PlayerWidget


class GameWindow(Window):
    """Shows a game of go

    :signal configure_game(): Request to show the game configuration window
    """
    configure_game = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.game = Game()

        self.status_widget = StatusWidget(['', ''])
        self.boardWidget = BoardWidget()
        self.result_widget = ResultWidget()
        self.playerWidgets = [PlayerWidget('', QPixmap('icons/blackStone.png'), parent=self),
                              PlayerWidget('', QPixmap('icons/whiteStone.png'), parent=self)]
        self.actionsWidget = ActionsWidget()
        self.analyze_widget = AnalyzeWidget()
        self.placeholder_widget = QWidget()

        self.menuBar().new_game.connect(self.configure_game.emit)
        self.menuBar().restart.connect(self.game.restart)
        self.menuBar().show_game_menu(True)

        self.connect_widgets()

        self.central_widget = QWidget()
        self.central_layout = QGridLayout()
        self.central_widget.setLayout(self.central_layout)
        self.central_layout.setSpacing(20)
        self.setCentralWidget(self.central_widget)

    def connect_widgets(self):
        self.boardWidget.clicked_field.connect(self.game.place_stone)

        self.game.invalid_move.connect(self.boardWidget.show_invalid_move)
        self.game.board_state_changed.connect(self.boardWidget.set_state)
        self.game.player_states_changed.connect(self.player_states_changed)
        self.game.game_status_changed.connect(self.game_status_changed)
        self.actionsWidget.restart.connect(self.game.restart)
        self.actionsWidget.pass_stone.connect(self.game.pass_stone)

        self.result_widget.new_game.connect(self.configure_game)
        self.result_widget.analyze.connect(self.show_analysis_layout)

        self.analyze_widget.show_step.connect(self.game.rewind)
        self.analyze_widget.new_game.connect(self.configure_game)

    def game_status_changed(self, game_status: GameStatus):
        """Show the game end layout if the game ended

        :param status: current GameStatus
        """
        if is_end_status(game_status):
            self.show_game_end_layout()
        self.status_widget.set_status(game_status, self.game.get_winner_status())

    def player_states_changed(self, states):
        self.playerWidgets[0].set_state(states[0])
        self.playerWidgets[1].set_state(states[1])

    def show_game_layout(self, conf: GameConfiguration):
        self.clear_layout()
        # Create new Status/PlayerWidgets with updated names
        self.playerWidgets[0] = PlayerWidget(conf.names[0], QPixmap('icons/blackStone.png'))
        self.playerWidgets[1] = PlayerWidget(conf.names[1], QPixmap('icons/whiteStone.png'))
        self.status_widget = StatusWidget(conf.names)

        self.central_layout.addWidget(self.playerWidgets[0], 0, 0, 2, 1, Qt.AlignTop)
        self.central_layout.addWidget(self.status_widget, 0, 1)
        self.central_layout.addWidget(self.playerWidgets[1], 0, 2, 2, 1, Qt.AlignTop)
        self.central_layout.addWidget(self.boardWidget, 1, 1)
        self.central_layout.addWidget(self.actionsWidget, 2, 1, Qt.AlignCenter)

        self.central_widget.setLayout(self.central_widget.layout())

        # Remove the darkened board from the game end layout
        self.boardWidget.highlight_fields(None)
        self.game.start_new_game(conf)

    def show_game_end_layout(self):
        self.clear_layout()
        self.central_layout.addWidget(self.playerWidgets[0], 0, 0, 2, 1, Qt.AlignTop)
        self.central_layout.addWidget(self.status_widget, 0, 1)
        self.central_layout.addWidget(self.playerWidgets[1], 0, 2, 2, 1, Qt.AlignTop)
        self.central_layout.addWidget(self.boardWidget, 1, 1)
        self.central_layout.addWidget(self.result_widget, 1, 1)

        # Darken the board to improve contrast to the action buttons on the field
        self.boardWidget.highlight_fields([])

    def show_analysis_layout(self):
        self.clear_layout()
        self.central_layout.addWidget(self.playerWidgets[0], 0, 0, 2, 1, Qt.AlignTop)
        self.central_layout.addWidget(self.status_widget, 0, 1)
        self.central_layout.addWidget(self.playerWidgets[1], 0, 2, 2, 1, Qt.AlignTop)
        self.central_layout.addWidget(self.boardWidget, 1, 1)
        self.central_layout.addWidget(self.analyze_widget, 2, 1, Qt.AlignCenter)

        self.boardWidget.highlight_fields(None)
        self.analyze_widget.set_history_steps(len(self.game.history) - 1)

    def clear_layout(self):
        """Remove all widgets from the current layout"""
        widgets = [self.playerWidgets[0], self.playerWidgets[1], self.status_widget,
                   self.boardWidget, self.actionsWidget, self.analyze_widget, self.result_widget]
        for widget in widgets:
            self.layout().removeWidget(widget)
            widget.setParent(self.placeholder_widget)
