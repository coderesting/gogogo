from PyQt5.QtWidgets import QWidget


class Game(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def calculate_score(self): pass

    def calculate_game_state(self): pass

    def calculate_next_board_state(self, row: int, col: int): pass

    def reset(self): pass
