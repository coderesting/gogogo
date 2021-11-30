from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout

from ActionsWidget import ActionsWidget
from BoardWidget import BoardWidget
from Game import Game
from PlayerWidget import PlayerWidget
from StatusWidget import StatusWidget


class GoApplication(QMainWindow):

    def __init__(self):
        super().__init__()
        self.status_widget = StatusWidget()
        self.boardWidget = BoardWidget()
        self.playerWidgets = [PlayerWidget('Tom', QColor('white'), parent=self),
                              PlayerWidget('Ellie', QColor('black'), parent=self)]
        self.actionsWidget = ActionsWidget()

        self.game = Game()

        center_layout = QVBoxLayout()
        center_layout.addWidget(self.status_widget)
        center_layout.addWidget(self.boardWidget)
        center_layout.addWidget(self.actionsWidget)

        window_layout = QHBoxLayout()
        window_layout.addWidget(self.playerWidgets[0])
        window_layout.addLayout(center_layout)
        window_layout.addWidget(self.playerWidgets[1])

        central_widget = QWidget()
        central_widget.setLayout(window_layout)
        self.setCentralWidget(central_widget)

        self.setWindowTitle('Go go go')
        self.show()
