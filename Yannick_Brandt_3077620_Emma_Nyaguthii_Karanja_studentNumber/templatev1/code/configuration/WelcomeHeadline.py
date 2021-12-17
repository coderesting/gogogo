from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout


class WelcomeHeadline(QWidget):
    def __init__(self):
        super().__init__()
        welcome_label = QLabel("Welcome to GoGoGo")
        welcome_label.setStyleSheet("font-size: 20px")
        welcome_label.setAlignment(Qt.AlignCenter)

        black_welcome_stone = QLabel()
        black_welcome_stone.setPixmap(QPixmap('icons/blackStone.png').scaledToWidth(30, Qt.SmoothTransformation))
        black_welcome_stone.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        white_welcome_stone = QLabel()
        white_welcome_stone.setPixmap(QPixmap('icons/whiteStone.png').scaledToWidth(30, Qt.SmoothTransformation))
        white_welcome_stone.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        welcome_layout = QHBoxLayout()
        welcome_layout.addStretch()
        welcome_layout.addWidget(black_welcome_stone)
        welcome_layout.addWidget(welcome_label)
        welcome_layout.addWidget(white_welcome_stone)
        welcome_layout.addStretch()
        welcome_layout.setContentsMargins(10, 10, 10, 10)

        self.setLayout(welcome_layout)
