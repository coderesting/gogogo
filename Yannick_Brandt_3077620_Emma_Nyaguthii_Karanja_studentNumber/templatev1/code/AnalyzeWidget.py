from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt5.QtWidgets import QWidget, QSlider, QLabel, QPushButton, QGridLayout


class AnalyzeWidget(QWidget):
    show_step = pyqtSignal(int)
    new_game = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        scroll_hint = QLabel("Step through the game")
        scroll_hint.setAlignment(Qt.AlignCenter)
        scroll_hint.setContentsMargins(10, 10, 10, 10)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.valueChanged.connect(self.show_step)

        new_game_button = QPushButton("New Game")
        new_game_button.clicked.connect(self.new_game)

        self.anim = QPropertyAnimation(self.slider, b"value")
        self.anim.setEndValue(0)
        self.anim.setEasingCurve(QEasingCurve.OutQuart)

        layout = QGridLayout()
        layout.addWidget(scroll_hint, 0, 0, 1, 3)
        layout.addWidget(QLabel('Start'), 1, 0)
        layout.addWidget(self.slider, 1, 1)
        layout.addWidget(QLabel('End'), 1, 2)
        layout.addWidget(new_game_button, 2, 0, 1, 3)

        self.setLayout(layout)

    def set_history_steps(self, steps: int):
        self.slider.setMaximum(steps)
        self.anim.setStartValue(steps)
        duration = max(min(steps * 100, 100), 3000)
        self.anim.setDuration(duration)
        self.anim.start()
