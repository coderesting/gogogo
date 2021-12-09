from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt5.QtWidgets import QWidget, QSlider, QLabel, QPushButton, QGridLayout


class AnalyzeWidget(QWidget):
    show_step = pyqtSignal(int)
    new_game = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.valueChanged.connect(self.show_step)

        new_game_button = QPushButton("New Game")
        new_game_button.clicked.connect(self.new_game)

        self.anim = QPropertyAnimation(self.slider, b"value")
        self.anim.setEndValue(0)
        self.anim.setEasingCurve(QEasingCurve.OutQuart)

        layout = QGridLayout()
        layout.addWidget(QLabel('Start'), 0, 0)
        layout.addWidget(self.slider, 0, 1)
        layout.addWidget(QLabel('End'), 0, 2)
        layout.addWidget(new_game_button, 1, 0, 1, 3)

        self.setLayout(layout)

    def set_history_steps(self, steps: int):
        self.slider.setMaximum(steps)
        self.anim.setStartValue(steps)
        duration = max(min(steps * 100, 1000), 3000)
        self.anim.setDuration(duration)
        self.anim.start()
