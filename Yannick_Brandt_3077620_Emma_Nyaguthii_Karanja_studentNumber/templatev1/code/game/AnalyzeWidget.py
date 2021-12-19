from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QSlider, QLabel, QHBoxLayout, QVBoxLayout, QPushButton

from BigButton import BigButton


class AnalyzeWidget(QWidget):
    """Shows controls to step through the game

    :signal show_step(int): Request to rewind the game to the specified step
    :signal new_game(): Request to start a new game
    """
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

        # Scroll the slider in the beginning to indicate the ability to step through the game
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
        """Step one step back"""
        self.slider.setValue(self.slider.value() - 1)

    def next(self):
        """Step one step forward"""
        self.slider.setValue(self.slider.value() + 1)

    def step_changed(self, value):
        """The value of the slider changed"""
        self.back_button.setDisabled(False)
        self.next_button.setDisabled(False)

        if value == 0:
            self.back_button.setDisabled(True)
        if value == self.slider.maximum():
            self.next_button.setDisabled(True)

        self.show_step.emit(value)

    def set_history_steps(self, steps: int):
        """Set the number of steps for in the current game"""
        self.slider.setMaximum(steps)
        self.anim.setStartValue(steps)
        duration = max(steps * 100, 3000)
        self.anim.setDuration(duration)
        self.anim.start()
        if steps == 0:
            self.step_changed(0)
