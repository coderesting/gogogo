from PyQt5.QtCore import QRect, pyqtSignal, QPropertyAnimation, QEasingCurve, pyqtProperty, QMargins, Qt
from PyQt5.QtGui import QResizeEvent, QMouseEvent, QPainter, QPaintEvent, QImage, QPen, QColor
from PyQt5.QtWidgets import QWidget, QSizePolicy

from BoardState import BoardState
from Field import Field


class BoardWidget(QWidget):
    """ This widget draws a go board and stones depending on a BoardState to the screen.

    :signal clicked_field(field:Field): user clicked on a field. It is not checked if the move is valid
    """
    clicked_field = pyqtSignal(Field)

    state = BoardState()
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
        for field in self.state:
            if self.get_field_rect(field).contains(evt.x(), evt.y()):
                self.clicked_field.emit(field)
                return

    def set_state(self, state):
        self.state = state
        self.update()

    def show_invalid_move(self, field: Field):
        """ Shows a red cross over a field to indicate an invalid move
        :param field: field to draw the cross over
        """
        self.invalid_field = field
        self.anim.stop()
        self.anim.start()

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.drawImage(self.board_rect, QImage('assets/board.png'))
        self.draw_stones(painter)
        if self.invalid_field:
            self.draw_invalid_field(painter, self.invalid_field)

    def draw_stones(self, painter: QPainter):
        """ Checks every field and draws a white or black stone depending on the board state
        :param painter: QPainter to draw on
        """
        for field in self.state:
            if self.state.get_field_value(field) == 0:
                self.draw_stone(painter, field, QImage('assets/blackStone.png'))
            elif self.state.get_field_value(field) == 1:
                self.draw_stone(painter, field, QImage('assets/whiteStone.png'))

    def draw_stone(self, painter: QPainter, field: Field, image: QImage):
        """ Draws a stone image in the specified position
        :param painter: QPainter to draw on
        :param field: field to place the stone in
        :param image: square QImage of the stone to draw
        """
        field_rect = self.get_field_rect(field)
        # create margins with same space (field_padding) in all directions
        field_margins = QMargins() + self.field_padding
        painter.drawImage(field_rect - field_margins, image)

    def get_field_rect(self, field: Field) -> QRect:
        """ Calculates a QRect for a given board position
        :param field: field to calculate rect for
        """
        x = self.board_rect.x() + self.board_padding + field.col * self.field_width
        y = self.board_rect.y() + self.board_padding + field.row * self.field_width
        return QRect(x, y, self.field_width, self.field_width)

    def draw_invalid_field(self, painter: QPainter, field: Field):
        """ Draws a red cross over a field to indicate an invalid move
        :param painter: QPainter to draw on
        :param field: field to draw the cross over
        """
        field_margins = QMargins() + self.field_padding
        field_rect = self.get_field_rect(field) - field_margins
        # transform the invalidFieldState (0-100) to opacity values (0-255-0)
        opacity = (-51 / 500) * pow(self._invalid_field_state, 2) + (51 / 5) * self._invalid_field_state
        pen = QPen(QColor(255, 0, 0, opacity), self.field_padding * 1.5)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        painter.drawLine(field_rect.topLeft(), field_rect.bottomRight())
        painter.drawLine(field_rect.topRight(), field_rect.bottomLeft())
