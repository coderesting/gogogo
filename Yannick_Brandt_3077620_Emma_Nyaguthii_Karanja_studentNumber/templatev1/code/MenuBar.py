"""
Name: Yannick Brandt
Student number: 3077620
"""

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMenuBar, QAction


class MenuBar(QMenuBar):
    """
       Provides the menu with help/about windows

       :signal show_tutorial(): request to open the tutorial
       :signal show_about(): request to open about
    """
    show_tutorial = pyqtSignal()
    show_about = pyqtSignal()
    restart = pyqtSignal()
    new_game = pyqtSignal()
    exit = pyqtSignal()

    def __init__(self):
        super().__init__()

        game_menu = self.addMenu("Game")

        self.restart_action = QAction(QIcon('./icons/restart.png'), 'Restart', self)
        self.restart_action.setShortcut('Ctrl+r')
        self.restart_action.triggered.connect(self.restart.emit)
        game_menu.addAction(self.restart_action)

        self.new_game_action = QAction(QIcon('./icons/newGame.png'), 'New Game', self)
        self.new_game_action.setShortcut('Ctrl+n')
        self.new_game_action.triggered.connect(self.new_game.emit)
        game_menu.addAction(self.new_game_action)

        self.exit_action = QAction(QIcon('./icons/exit.png'), 'Quit', self)
        self.exit_action.setShortcut('Ctrl+q')
        self.exit_action.triggered.connect(self.exit.emit)
        game_menu.addAction(self.exit_action)

        help_menu = self.addMenu('​Help')

        # help menu item. Space is required to prevent macOS from moving this to another location
        help_action = QAction(QIcon('./icons/help.png'), 'How to play', self)
        help_action.setShortcut('Ctrl+?')
        help_action.triggered.connect(self.show_tutorial.emit)
        help_menu.addAction(help_action)

        # about menu item. Space is required to prevent macOS from moving this to another location
        about_action = QAction(QIcon('./icons/app.png'), '​About​', self)
        about_action.setShortcut('Ctrl+A')
        about_action.triggered.connect(self.show_about.emit)
        help_menu.addAction(about_action)

    def show_game_menu(self, show_game_menu):
        self.restart_action.setDisabled(not show_game_menu)
        self.new_game_action.setDisabled(not show_game_menu)
