from board.BoardState import BoardState


class TutorialStep():
    """Represents one step in the tutorial"""

    def __init__(self, title: str, description: str, board_state: BoardState, field_to_click, show_invalid_move):
        self.title = title
        self.description = description
        self.board_state = board_state
        self.field_to_click = field_to_click
        self.show_invalid_move = show_invalid_move
