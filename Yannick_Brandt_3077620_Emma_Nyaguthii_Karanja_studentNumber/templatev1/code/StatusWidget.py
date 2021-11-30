from PyQt5.QtWidgets import QWidget


class StatusWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_status(self, status:str): pass
