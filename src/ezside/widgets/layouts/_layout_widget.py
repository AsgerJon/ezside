"""LayoutWidget is meant to provide the central widget that has a layout
assigned to it before a QMainWindow makes it the central widget.
Typically, a simple QWidget instance may be used, but a subclass such as
this can be made to provide additional functionality. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QPaintEvent, QPainter, QBrush, QColor

from ezside.core import Tight, SolidFill, emptyPen
from ezside.widgets import BaseWidget


class LayoutWidget(BaseWidget):
  """LayoutWidget is meant to provide the central widget that has a layout
  assigned to it before a QMainWindow makes it the central widget.
  Typically, a simple QWidget instance may be used, but a subclass such as
  this can be made to provide additional functionality. """

  def initUi(self) -> None:
    """Initialize the user interface."""
    self.setSizePolicy(Tight, Tight)

  def paintEvent(self, event: QPaintEvent) -> None:
    """Paint the widget."""
    painter = QPainter()
    painter.begin(self)
    debugBrush = QBrush()
    debugBrush.setColor(QColor(144, 255, 0, 63))
    debugBrush.setStyle(SolidFill)
    painter.setBrush(debugBrush)
    painter.setPen(emptyPen())
    painter.drawRect(painter.viewport())
    painter.end()
