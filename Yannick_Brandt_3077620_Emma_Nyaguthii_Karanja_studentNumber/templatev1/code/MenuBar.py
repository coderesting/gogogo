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

    def __init__(self):
        super().__init__()

        help_menu = self.addMenu('​Help')

        # help menu item. Space is required to prevent macOS from moving this to another location
        helpAction = QAction(QIcon('./icons/help.png'), 'How to play', self)
        helpAction.setShortcut('Ctrl+?')
        helpAction.triggered.connect(self.show_tutorial.emit)
        help_menu.addAction(helpAction)

        # about menu item. Space is required to prevent macOS from moving this to another location
        aboutAction = QAction(QIcon('./icons/app.png'), '​About​', self)
        aboutAction.setShortcut('Ctrl+A')
        aboutAction.triggered.connect(self.show_about.emit)
        help_menu.addAction(aboutAction)
