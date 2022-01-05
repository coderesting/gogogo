from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QComboBox


class HandicapInput(QWidget):
    """Lets the user chose a handicap for the game"""

    def __init__(self):
        super().__init__()

        self.handicap_input = QComboBox()
        self.handicap_input.addItem('No Handicap', 0)
        self.handicap_input.addItem('6.5 Points', 6.5)
        self.handicap_input.addItem('7.5 Points', 7.5)

        handicap_label = QLabel("Handicap (extra points for white)")
        handicap_label.setStyleSheet('font-size:13px')

        handicap_layout = QVBoxLayout()
        handicap_layout.setAlignment(Qt.AlignCenter)
        handicap_layout.setSpacing(10)
        handicap_layout.addWidget(handicap_label)
        handicap_layout.addWidget(self.handicap_input)
        handicap_layout.setContentsMargins(5, 0, 5, 20)
        self.setLayout(handicap_layout)

    def get_handicap(self):
        return self.handicap_input.currentData()
