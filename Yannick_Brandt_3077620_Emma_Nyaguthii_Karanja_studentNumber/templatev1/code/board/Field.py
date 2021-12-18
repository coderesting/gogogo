class Field:
    """Represents a field on the go board"""

    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col

    def __eq__(self, obj):
        """Two fields are equal if their row and colum match"""
        return isinstance(obj, Field) and obj.row == self.row and obj.col == self.col

    def neighbors(self):
        """
        :returns: an array of neighbor fields
        """
        neighbors = []
        # Top neighbor
        if self.row > 0:
            neighbors.append(Field(self.row - 1, self.col))
        # Left neighbor
        if self.col > 0:
            neighbors.append(Field(self.row, self.col - 1))
        # Right neighbor
        if self.col < 6:
            neighbors.append(Field(self.row, self.col + 1))
        # Bottom neighbor
        if self.row < 6:
            neighbors.append(Field(self.row + 1, self.col))
        return neighbors
