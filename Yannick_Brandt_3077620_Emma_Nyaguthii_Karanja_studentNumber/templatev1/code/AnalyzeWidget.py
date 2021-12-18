from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QSlider, QLabel, QHBoxLayout, QVBoxLayout, QPushButton

from BigButton import BigButton


class AnalyzeWidget(QWidget):
    show_step = pyqtSignal(int)
    new_game = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        scroll_hint = QLabel("Step through the game")
        scroll_hint.setStyleSheet('font-size: 14px;')
        scroll_hint.setAlignment(Qt.AlignCenter)
        scroll_hint.setContentsMargins(0, 10, 0, 0)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.valueChanged.connect(self.step_changed)

        new_game_button = BigButton("New Game")
        new_game_button.clicked.connect(self.new_game)

        self.anim = QPropertyAnimation(self.slider, b"value")
        self.anim.setEndValue(0)
        self.anim.setEasingCurve(QEasingCurve.OutQuart)

        self.back_button = QPushButton()
        self.back_button.setIcon(QIcon('icons/back.png'))
        self.back_button.clicked.connect(self.back)

        self.next_button = QPushButton()
        self.next_button.setIcon(QIcon('icons/next.png'))
        self.next_button.clicked.connect(self.next)

        slider_layout = QHBoxLayout()
        slider_layout.addWidget(self.back_button)
        slider_layout.addWidget(self.slider)
        slider_layout.addWidget(self.next_button)

        analyze_layout = QVBoxLayout()
        analyze_layout.setSpacing(20)
        analyze_layout.addWidget(scroll_hint)
        analyze_layout.addLayout(slider_layout)
        analyze_layout.addWidget(new_game_button)

        self.setLayout(analyze_layout)
        self.setMinimumWidth(300)
        self.setMaximumWidth(600)

    def back(self):
        self.slider.setValue(self.slider.value() - 1)

    def next(self):
        self.slider.setValue(self.slider.value() + 1)

    def step_changed(self, value):
        self.back_button.setDisabled(False)
        self.next_button.setDisabled(False)

        if value == 0:
            self.back_button.setDisabled(True)
        if value == self.slider.maximum():
            self.next_button.setDisabled(True)

        self.show_step.emit(value)

    def set_history_steps(self, steps: int):
        self.slider.setMaximum(steps)
        self.anim.setStartValue(steps)
        duration = max(min(steps * 100, 100), 3000)
        self.anim.setDuration(duration)
        self.anim.start()
