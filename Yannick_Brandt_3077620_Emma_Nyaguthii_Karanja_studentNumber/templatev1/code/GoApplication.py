from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout

from ActionsWidget import ActionsWidget
from BoardWidget import BoardWidget
from Game import Game
from PlayerWidget import PlayerWidget
from StatusWidget import StatusWidget


class GoApplication(QMainWindow):

    def __init__(self):
        super().__init__()
        self.game = Game()

        self.status_widget = StatusWidget()
        self.boardWidget = BoardWidget()
        self.playerWidgets = [PlayerWidget('Tom', QColor('white'), parent=self),
                              PlayerWidget('Ellie', QColor('black'), parent=self)]
        self.actionsWidget = ActionsWidget()

        self.connect_widgets()

        self.create_layout()

        self.setWindowTitle('Go go go')
        self.setWindowIcon(QIcon('assets/appIcon.png'))
        self.show()

    def connect_widgets(self):
        self.boardWidget.clicked_field.connect(self.game.place_stone)
        self.game.invalid_move.connect(self.boardWidget.show_invalid_move)
        self.game.board_state_changed.connect(self.boardWidget.set_state)
        self.game.player_state_changed.connect(lambda idx, state: self.playerWidgets[idx].set_state(state))
        self.game.game_state_changed.connect(self.status_widget.set_status)

    def create_layout(self):
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.playerWidgets[0], 0, 0)
        grid_layout.addWidget(self.status_widget, 0, 1)
        grid_layout.addWidget(self.playerWidgets[1], 0, 2)
        grid_layout.addWidget(self.boardWidget, 1, 1)
        grid_layout.addWidget(self.actionsWidget, 2, 1)

        central_widget = QWidget()
        central_widget.setLayout(grid_layout)
        self.setCentralWidget(central_widget)
