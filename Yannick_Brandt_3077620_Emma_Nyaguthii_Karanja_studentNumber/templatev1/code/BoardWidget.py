from PyQt5.QtCore import QRect, pyqtSignal, QMargins, pyqtProperty, QPropertyAnimation, QEasingCurve, Qt
from PyQt5.QtGui import QMouseEvent, QPainter, QPaintEvent, QImage, QResizeEvent, QColor, QPen
from PyQt5.QtWidgets import QWidget, QSizePolicy


class BoardWidget(QWidget):
    """ This widget represents a go game board + stones.
    The board state is represented by a 7x7 two dimensional array.
    Example:
    [0, 0, 1, 1, 1, 1, 0]
    [0, 0, 0, 2, 1, 1, 0]
    [0, 0, 2, 0, 0, 0, 0]
    [0, 2, 0, 2, 0, 0, 0]
    [0, 0, 2, 2, 0, 0, 0]
    [0, 0, 0, 0, 0, 0, 0]
    [0, 0, 0, 0, 0, 0, 0]
    0 = free field
    1 = white stone
    2 = black stone

    :signal clicked_field(row:int, col:int): user clicked on a field. It is not checked if the move is valid
    """
    clicked_field = pyqtSignal(int, int)

    state = [[0] * 7 for i in range(7)]
    board_rect = QRect()
    board_padding: float
    field_width: float
    field_padding: float
    invalid_field = None
    _invalid_field_state = 0

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        # create an animation to show an invalid move
        self.anim = QPropertyAnimation(self, b"invalid_field_state")
        self.anim.setDuration(1000)
        self.anim.setStartValue(0)
        self.anim.setEndValue(100)
        self.anim.setEasingCurve(QEasingCurve.OutQuart)

        self.setMinimumSize(300, 300)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    # custom property to animate an invalid move
    def get_invalid_field_state(self):
        return self._invalid_field_state

    def set_invalid_field_state(self, value):
        self._invalid_field_state = value
        self.update()

    invalid_field_state = pyqtProperty(int, get_invalid_field_state, set_invalid_field_state)

    def resizeEvent(self, evt: QResizeEvent):
        # calculate variables to display the board as a square in the widget
        board_length = min(self.width(), self.height())
        board_x = 0
        board_y = 0
        if self.width() > self.height():
            board_x = self.width() / 2 - board_length / 2
        else:
            board_y = self.height() / 2 - board_length / 2

        self.board_rect = QRect(board_x, board_y, board_length, board_length)

        self.board_padding = board_length / 60
        self.field_padding = board_length / 60
        self.field_width = (board_length - self.board_padding * 2) / 7

    def mousePressEvent(self, evt: QMouseEvent):
        # Check every field for a collision with the mouse
        for row in range(7):
            for col in range(7):
                if self.get_field_rect(row, col).contains(evt.x(), evt.y()):
                    self.clicked_field.emit(row, col)
                    return

    def set_state(self, state):
        self.state = state
        self.update()

    def show_invalid_move(self, row, col):
        """ Shows a red cross over a field to indicate an invalid move
        :param row: row to draw the cross over [0-6]
        :param col: column to draw the cross over [0-6]
        """
        self.invalid_field = [row, col]
        self.anim.stop()
        self.anim.start()

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.drawImage(self.board_rect, QImage('assets/board.png'))
        self.draw_stones(painter)
        if self.invalid_field:
            self.draw_invalid_field(painter, self.invalid_field[0], self.invalid_field[1])

    def draw_stones(self, painter: QPainter):
        """ Checks every field and draws a white or black stone depending on the board state
        :param painter: QPainter to draw on
        """
        for row in range(7):
            for col in range(7):
                field = self.state[row][col]
                if field == 1:
                    self.draw_stone(painter, row, col, QImage('assets/whiteStone.png'))
                elif field == 2:
                    self.draw_stone(painter, row, col, QImage('assets/blackStone.png'))

    def draw_stone(self, painter: QPainter, row: int, col: int, image: QImage):
        """ Draws a stone image in the specified position
        :param painter: QPainter to draw on
        :param row: row to place the stone in [0-6]
        :param col: column to place the stone in [0-6]
        :param image: square QImage of the stone to draw
        """
        field_rect = self.get_field_rect(row, col)
        # create margins with same space (field_padding) in all directions
        field_margins = QMargins() + self.field_padding
        painter.drawImage(field_rect - field_margins, image)

    def get_field_rect(self, row: int, col: int) -> QRect:
        """ Calculates a QRect for a given board position
        :param row: row to calculate rect for [0-6]
        :param col: column to calculate rect for [0-6]
        """
        x = self.board_rect.x() + self.board_padding + row * self.field_width
        y = self.board_rect.y() + self.board_padding + col * self.field_width
        return QRect(x, y, self.field_width, self.field_width)

    def draw_invalid_field(self, painter: QPainter, row: int, col: int):
        """ Draws a red cross over a field to indicate an invalid move
        :param painter: QPainter to draw on
        :param row: row to draw the cross over [0-6]
        :param col: column to draw the cross over [0-6]
        """
        field_margins = QMargins() + self.field_padding
        field_rect = self.get_field_rect(row, col) - field_margins
        # transform the invalidFieldState (0-100) to opacity values (0-255-0)
        opacity = (-51 / 500) * pow(self._invalid_field_state, 2) + (51 / 5) * self._invalid_field_state
        pen = QPen(QColor(255, 0, 0, opacity), self.field_padding * 1.5)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        painter.drawLine(field_rect.topLeft(), field_rect.bottomRight())
        painter.drawLine(field_rect.topRight(), field_rect.bottomLeft())
