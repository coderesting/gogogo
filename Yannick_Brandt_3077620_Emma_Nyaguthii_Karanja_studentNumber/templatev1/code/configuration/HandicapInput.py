from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QButtonGroup, QHBoxLayout, QPushButton


class HandicapInput(QWidget):
    change = pyqtSignal(object)

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

        # Forward the change event
        self.handicap_group.buttonToggled.connect(self.change.emit)

        h_box = QHBoxLayout()
        h_box.addWidget(no_button)
        h_box.addWidget(plus6_5_button)
        h_box.addWidget(plus_7_5_button)
        self.setLayout(h_box)

    def get_handicap(self):
        return self.handicap_group.checkedButton().data

    def set_handicap(self, handicap):
        for button in self.handicap_group.buttons():
            if button.data == handicap:
                button.setChecked(True)
