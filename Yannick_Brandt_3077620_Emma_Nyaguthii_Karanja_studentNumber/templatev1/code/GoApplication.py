import random

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

        self.boardWidget.clicked_field.connect(self.play_move)

        grid_layout = QGridLayout()
        grid_layout.addWidget(self.playerWidgets[0], 0, 0)
        grid_layout.addWidget(self.status_widget, 0, 1)
        grid_layout.addWidget(self.playerWidgets[1], 0, 2)
        grid_layout.addWidget(self.boardWidget, 1, 1)
        grid_layout.addWidget(self.actionsWidget, 2, 1)

        central_widget = QWidget()
        central_widget.setLayout(grid_layout)
        self.setCentralWidget(central_widget)

        self.setWindowTitle('Go go go')
        self.show()

    # For testing purposes only
    def play_move(self, row: int, col: int):
        if random.randint(0, 1):
            self.boardWidget.show_invalid_move(row, col)
        else:
            self.boardWidget.state[row][col] = random.randint(1, 2)
            self.boardWidget.set_state(self.boardWidget.state)
