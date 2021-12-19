from PyQt5.QtCore import pyqtSignal, QRectF, QMarginsF
from PyQt5.QtGui import QResizeEvent, QMouseEvent, QPainter, QPaintEvent, QImage, QColor, QPainterPath, QBrush
from PyQt5.QtWidgets import QWidget, QSizePolicy

from board.BoardState import BoardState
from board.Field import Field
from board.RedCross import RedCross


class BoardWidget(QWidget):
    """ This widget draws a go board and stones depending on a BoardState to the screen.

    :signal clicked_field(field:Field): user clicked on a field. It is not checked if the move is valid
    """
    clicked_field = pyqtSignal(Field)

    state = BoardState()

    # Values to draw the board and stones
    board_rect = QRectF()
    board_padding: float
    field_width: float
    field_padding: float

    highlighted_fields = None

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.red_cross = RedCross()
        self.red_cross.change.connect(self.update)

        self.setMinimumSize(400, 400)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def resizeEvent(self, evt: QResizeEvent):
        # calculate variables to display the board as a square in the widget
        board_length = min(self.width(), self.height())
        board_x = 0
        board_y = 0
        if self.width() > self.height():
            board_x = self.width() / 2 - board_length / 2
        else:
            board_y = self.height() / 2 - board_length / 2

        self.board_rect = QRectF(board_x, board_y, board_length, board_length)

        self.board_padding = board_length / 78
        self.field_padding = board_length / 60
        self.field_width = (board_length - self.board_padding * 2) / 7

    def mousePressEvent(self, evt: QMouseEvent):
        # Check every field for a collision with the mouse
        for field in self.state:
            if self.get_field_rect(field).contains(evt.x(), evt.y()):
                self.clicked_field.emit(field)
                return

    def set_state(self, state: BoardState):
        self.state = state
        self.update()

    def highlight_fields(self, fields):
        self.highlighted_fields = fields
        self.update()

    def show_invalid_move(self, field: Field):
        """ Shows a red cross over a field to indicate an invalid move
        :param field: field to draw the cross on
        """
        self.red_cross.show_at(field)

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        painter.drawImage(self.board_rect, QImage('icons/board.png'))

        self.draw_stones(painter)

        if self.red_cross.field:
            self.red_cross.draw(painter, self.get_field_rect(self.red_cross.field), self.field_padding)

        if self.highlighted_fields is not None:
            self.draw_highlighted_fields(painter)

    def draw_stones(self, painter: QPainter):
        """ Checks every field and draws a white or black stone_pixmap depending on the board status
        :param painter: QPainter to draw on
        """
        for field in self.state:
            if self.state.get_field_value(field) == 0:
                self.draw_stone(painter, field, QImage('icons/blackStone.png'))
            elif self.state.get_field_value(field) == 1:
                self.draw_stone(painter, field, QImage('icons/whiteStone.png'))

    def draw_stone(self, painter: QPainter, field: Field, image: QImage):
        """ Draws a stone_pixmap image in the specified position
        :param painter: QPainter to draw on
        :param field: field to place the stone_pixmap in
        :param image: square QImage of the stone_pixmap to draw
        """
        field_rect = self.get_field_rect(field)
        # create margins with same space (field_padding) in all directions
        field_margins = QMarginsF() + self.field_padding
        painter.drawImage(field_rect - field_margins, image)

    def get_field_rect(self, field: Field) -> QRectF:
        """ Calculates a QRect for a given board position
        :param field: field to calculate rect for
        """
        x = self.board_rect.x() + self.board_padding + field.col * self.field_width
        y = self.board_rect.y() + self.board_padding + field.row * self.field_width
        return QRectF(x, y, self.field_width, self.field_width)

    def draw_highlighted_fields(self, painter: QPainter):
        """Highlights a number of fields by drawing an ellipse around them

        :painter: QPainter to draw on
        """
        mask = QPainterPath()
        mask.addRect(self.board_rect)
        for field in self.highlighted_fields:
            mask.addEllipse(self.get_field_rect(field))
        painter.fillPath(mask, QBrush(QColor(0, 0, 0, 70)))
