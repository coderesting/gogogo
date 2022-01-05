from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QGridLayout

from configuration.inputs.InputErrorLabel import InputErrorLabel


class PlayerNameInput(QWidget):
    """Lets the user input two player names

    :signal error_state_changed(bool): True = There are errors in the names; False = No errors
    """
    error_state_changed = pyqtSignal(bool)

    def __init__(self):
        super().__init__()

        self.backup_names = ['Anonymous Wombat', 'Anonymous Raccoon']
        name_labels = [None, None]
        self.name_inputs = [None, None]
        self.error_labels = [InputErrorLabel(), InputErrorLabel()]

        name_labels[0] = QLabel("Player 1 (black)")
        self.name_inputs[0] = QLineEdit()
        self.name_inputs[0].setPlaceholderText("name")
        self.name_inputs[0].textChanged.connect(self.check_names)

        against_label = QLabel("-")

        name_labels[1] = QLabel("Player 2 (white)")
        self.name_inputs[1] = QLineEdit()
        self.name_inputs[1].setPlaceholderText("name")
        self.name_inputs[1].textChanged.connect(self.check_names)

        player_names_layout = QGridLayout()
        player_names_layout.addWidget(name_labels[0], 0, 0)
        player_names_layout.addWidget(self.name_inputs[0], 1, 0)
        player_names_layout.addWidget(self.error_labels[0], 2, 0)

        player_names_layout.addWidget(against_label, 1, 1)

        player_names_layout.addWidget(name_labels[1], 0, 2)
        player_names_layout.addWidget(self.name_inputs[1], 1, 2)
        player_names_layout.addWidget(self.error_labels[1], 2, 2)
        player_names_layout.setContentsMargins(5, 15, 5, 0)
        self.setLayout(player_names_layout)

        self.check_names()

    def check_names(self):
        """ Check if the names are valid and display an error message otherwise"""
        has_error = False
        for i in [0, 1]:
            if len(self.name_inputs[i].text()) > 15:
                self.error_labels[i].show_error("Name is too long")
                has_error = True
            else:
                self.error_labels[i].show_error(None)
        self.error_state_changed.emit(has_error)

    def get_player_names(self):
        names = [None, None]
        for i in [0, 1]:
            name = self.name_inputs[i].text().strip()
            # Use backup names (Anonymous x) if no name is provided
            names[i] = name if name else self.backup_names[i]
        return names
