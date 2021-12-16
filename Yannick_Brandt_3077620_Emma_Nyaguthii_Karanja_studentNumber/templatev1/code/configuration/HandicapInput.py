from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QButtonGroup, QHBoxLayout, QPushButton, QLabel, QVBoxLayout


class HandicapInput(QWidget):
    def __init__(self):
        super().__init__()

        # Create a join_type_group to ensure only one button is active
        self.handicap_group = QButtonGroup(self)

        no_button = QPushButton("None")
        # Set the data attribute to associate it later on click
        no_button.data = 0
        no_button.setToolTip("No handicap")
        no_button.setCheckable(True)
        self.handicap_group.addButton(no_button)
        # Select the ho handicap button because it is the one, users probably expect
        no_button.setChecked(True)

        plus6_5_button = QPushButton("+6.5 Points")
        plus6_5_button.data = 6.5
        plus6_5_button.setToolTip("White gets +6.5 points")
        plus6_5_button.setCheckable(True)
        self.handicap_group.addButton(plus6_5_button)

        plus_7_5_button = QPushButton("+7.5 Points")
        plus_7_5_button.data = 7.5
        plus_7_5_button.setToolTip("White gets +7.5 points")
        plus_7_5_button.setCheckable(True)
        self.handicap_group.addButton(plus_7_5_button)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(no_button)
        buttons_layout.addWidget(plus6_5_button)
        buttons_layout.addWidget(plus_7_5_button)

        handicap_label = QLabel("Handicap (extra points for white)")
        handicap_label.setAlignment(Qt.AlignCenter)
        handicap_label.setStyleSheet('font-size:13px')

        handicap_layout = QVBoxLayout()
        handicap_layout.setSpacing(10)
        handicap_layout.addWidget(handicap_label)
        handicap_layout.addLayout(buttons_layout)
        handicap_layout.setContentsMargins(5, 0, 5, 20)
        self.setLayout(handicap_layout)

    def get_handicap(self):
        return self.handicap_group.checkedButton().data
