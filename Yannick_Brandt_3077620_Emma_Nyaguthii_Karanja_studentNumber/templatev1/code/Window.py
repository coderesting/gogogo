from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow

from AboutWindow import AboutWindow
from MenuBar import MenuBar
from tutorial.TutorialWindow import TutorialWindow


class Window(QMainWindow):
    """Abstract class for both game and configuration window. Provides the menu and title/icon"""

    def __init__(self):
        super().__init__()

        self.about_window = AboutWindow(parent=self)
        self.tutorial_window = TutorialWindow(parent=self)

        menu_bar = MenuBar()
        menu_bar.show_game_menu(False)
        menu_bar.show_tutorial.connect(self.show_tutorial)
        menu_bar.show_about.connect(self.about_window.show)
        menu_bar.exit.connect(self.close)

        self.setMenuBar(menu_bar)

        self.setWindowTitle('GoGoGo')
        self.setWindowIcon(QIcon('icons/app.png'))

    def show_tutorial(self):
        self.tutorial_window.reset()
        self.tutorial_window.show()
