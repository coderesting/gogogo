from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QCheckBox, QSpinBox, QFormLayout, QSizePolicy


class TimerInput(QWidget):
    def __init__(self):
        super().__init__()

        self.timer_input = QSpinBox()
        self.timer_input.setSingleStep(1)
        self.timer_input.setMinimum(1)
        self.timer_input.setMaximum(500)
        self.timer_input.setValue(15)
        self.timer_input.setSuffix('min')
        self.timer_input.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.use_timer_checkbox = QCheckBox()
        self.use_timer_checkbox.setCheckState(2)
        self.use_timer_checkbox.stateChanged.connect(lambda val: self.timer_input.setDisabled(val == 0))

        input_layout = QFormLayout()
        input_layout.addRow("Use time limit:", self.use_timer_checkbox)
        input_layout.addRow("Time limit:", self.timer_input)

        timer_label = QLabel("Timelimit per player (across all moves)")
        timer_label.setAlignment(Qt.AlignCenter)
        timer_label.setStyleSheet('font-size:13px')

        timer_layout = QVBoxLayout()
        timer_layout.setSpacing(10)
        timer_layout.addWidget(timer_label)
        timer_layout.addLayout(input_layout)
        timer_layout.setContentsMargins(5, 15, 5, 15)
        self.setLayout(timer_layout)

    def get_time_limit(self):
        return self.timer_input.value() * 60 if self.use_timer_checkbox.checkState() == 2 else None
