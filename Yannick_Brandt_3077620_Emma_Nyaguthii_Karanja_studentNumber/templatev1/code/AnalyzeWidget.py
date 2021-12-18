from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt5.QtWidgets import QWidget, QSlider, QLabel, QHBoxLayout, QVBoxLayout

from BigButton import BigButton


class AnalyzeWidget(QWidget):
    show_step = pyqtSignal(int)
    new_game = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        scroll_hint = QLabel("Step through the game")
        scroll_hint.setStyleSheet('font-size: 14px;')
        scroll_hint.setAlignment(Qt.AlignCenter)
        scroll_hint.setContentsMargins(10, 10, 10, 10)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.valueChanged.connect(self.show_step)

        new_game_button = BigButton("New Game")
        new_game_button.clicked.connect(self.new_game)

        self.anim = QPropertyAnimation(self.slider, b"value")
        self.anim.setEndValue(0)
        self.anim.setEasingCurve(QEasingCurve.OutQuart)

        slider_layout = QHBoxLayout()
        slider_layout.addWidget(QLabel('Start'))
        slider_layout.addWidget(self.slider)
        slider_layout.addWidget(QLabel('End'))

        analyze_layout = QVBoxLayout()
        analyze_layout.setSpacing(10)
        analyze_layout.addWidget(scroll_hint)
        analyze_layout.addLayout(slider_layout)
        analyze_layout.addWidget(new_game_button)

        self.setLayout(analyze_layout)
        self.setMinimumWidth(300)
        self.setMaximumWidth(600)

    def set_history_steps(self, steps: int):
        self.slider.setMaximum(steps)
        self.anim.setStartValue(steps)
        duration = max(min(steps * 100, 100), 3000)
        self.anim.setDuration(duration)
        self.anim.start()
