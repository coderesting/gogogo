from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, pyqtSignal, Qt, QRect, pyqtProperty, QMarginsF
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtWidgets import QWidget

from board.Field import Field


class RedCross(QWidget):
    _invalid_field_state = 0
    field: Field = None
    change = pyqtSignal()

    def __init__(self):
        super().__init__()
        # create an animation to show an invalid move
        self.anim = QPropertyAnimation(self, b"invalid_field_state")
        self.anim.setDuration(1000)
        self.anim.setStartValue(0)
        self.anim.setEndValue(100)
        self.anim.setEasingCurve(QEasingCurve.OutQuart)

    # custom property to animate the red cross of an invalid move
    def get_invalid_field_state(self):
        return self._invalid_field_state

    def set_invalid_field_state(self, value):
        self._invalid_field_state = value
        self.change.emit()

    invalid_field_state = pyqtProperty(int, get_invalid_field_state, set_invalid_field_state)

    def show_at(self, field: Field):
        self.field = field
        self.anim.stop()
        self.anim.start()

    def draw(self, painter: QPainter, field_rect: QRect, field_padding: float):
        """ Draws a red cross over a field to indicate an invalid move
        :param painter: QPainter to draw on
        :param field_rect: QRect to draw the cross in
        :param field_padding: field padding
        """
        cross_rect = field_rect - (QMarginsF() + field_padding)
        # transform the invalidFieldState (0-100) to opacity values (0-255-0)
        opacity = (-51 / 500) * pow(self._invalid_field_state, 2) + (51 / 5) * self._invalid_field_state
        pen = QPen(QColor(255, 0, 0, opacity), field_padding * 1.5)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        painter.drawLine(cross_rect.topLeft(), cross_rect.bottomRight())
        painter.drawLine(cross_rect.topRight(), cross_rect.bottomLeft())
