from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QMessageBox

from BigButton import BigButton


class ActionsWidget(QWidget):
    """Shows restart and pass buttons

    :signal restart(): Request to restart the current game
    :signal pass_stone(): Request to pass a stone_pixmap
    """
    restart = pyqtSignal()
    pass_stone = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.restart_button = BigButton("Restart")
        self.restart_button.clicked.connect(self.restart_question)

        self.pass_button = BigButton("Pass")
        self.pass_button.clicked.connect(self.pass_stone.emit)

        layout = QHBoxLayout()
        layout.setSpacing(20)
        layout.addWidget(self.restart_button)
        layout.addWidget(self.pass_button)
        self.setLayout(layout)

        self.setMinimumWidth(300)

    def restart_question(self):
        message_box = QMessageBox()
        choice = message_box.question(self, 'Restart', "Do you really want to restart the game?",
                                      message_box.Yes | message_box.No)

        if choice == message_box.Yes:
            self.restart.emit()
