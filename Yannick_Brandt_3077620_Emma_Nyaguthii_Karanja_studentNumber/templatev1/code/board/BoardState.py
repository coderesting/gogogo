import copy

from board.Field import Field


class BoardState:
    """
    The board is represented by a 7x7 two dimensional array.
    Example:
    [[-1, -1,  1,  1,  1,  1, -1]
    [-1, -1, -1,  0,  1,  1, -1]
    [-1, -1,  0, -1, -1, -1, -1]
    [-1,  0, -1,  0, -1, -1, -1]
    [-1, -1,  0,  0, -1, -1, -1]
    [-1, -1, -1, -1, -1, -1, -1]
    [-1, -1, -1, -1, -1, -1, -1]]
    -1 = free field
    0 = black stone
    1 = white stone
    """

    def __init__(self):
        self.state = [[-1] * 7 for i in range(7)]
        self.iterator_field: Field

    def set_field_value(self, field: Field, value: int):
        """Sets the value of a field
        :field: Field to set the value for
        :value: -1 = free field
                0 = black stone
                1 = white stone
        """
        self.state[field.row][field.col] = value

    def get_field_value(self, field: Field):
        """
        :returns:   -1 = free field
                    0 = black stone
                    1 = white stone
        """
        return self.state[field.row][field.col]

    def clone(self):
        """Clones the BoardState"""
        board_state = BoardState()
        board_state.state = copy.deepcopy(self.state)
        return board_state

    # Make the board iterable (iterate over every field)
    def __iter__(self):
        self.iterator_field = Field(0, 0)
        return self

    def __next__(self):
        field = self.iterator_field
        if field == Field(7, 0):
            raise StopIteration
        if field.col > 5:
            self.iterator_field = Field(field.row + 1, 0)
        else:
            self.iterator_field = Field(field.row, field.col + 1)
        return field

    # Two boards are equal if all their field values are equal
    def __eq__(self, obj):
        if not isinstance(obj, BoardState):
            return False

        for i in range(7):
            for j in range(7):
                if self.state[i][j] != obj.state[i][j]:
                    return False

        return True
