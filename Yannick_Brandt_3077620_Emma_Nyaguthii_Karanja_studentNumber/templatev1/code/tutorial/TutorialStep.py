from board.BoardState import BoardState


class TutorialStep():
    def __init__(self, title, description, board_state: BoardState, field_to_click, show_invalid_move):
        self.title = title
        self.description = description
        self.board_state = board_state
        self.field_to_click = field_to_click
        self.show_invalid_move = show_invalid_move
