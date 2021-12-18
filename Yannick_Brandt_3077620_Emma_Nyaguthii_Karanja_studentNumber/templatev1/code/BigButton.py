from PyQt5.QtWidgets import QPushButton


class BigButton(QPushButton):

    def __init__(self, title):
        super().__init__(title)
        # self.setFont(QFont('Arial', 15))
