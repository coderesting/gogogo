from PyQt5.QtWidgets import QLabel


class InputErrorLabel(QLabel):
    """
    This widget shows an error message in a red box.
    It is normally invisible but occupies space to prevent main_layout shifts
    """

    def __init__(self):
        super().__init__()
        self.show_error(None)

    def show_error(self, message):
        """
        Show error message

        :param message: error message (None to hide the label)
        """
        if message is not None:
            self.setText(message)
            self.show()
        else:
            self.setText('')
            self.hide()

    def hide(self):
        # Occupy the same space as if the label was active to prevent main_layout shifts
        self.setStyleSheet('margin-bottom: 8px')

    def show(self):
        # Used the material design color system
        # Background: red 100
        # Border: red 500
        self.setStyleSheet(
            'background-color: #FFCDD2; border-radius: 5px; border: 1px solid #F44336; padding: 3px')
