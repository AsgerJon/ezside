"""ColonDisplay displays a colon. Used by digital clock widget. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QPointF
from PySide6.QtGui import QPainter
from icecream import ic

from ezside.widgets import SevenSegmentDigit

ic.configureOutput(includeContext=True, )


class ColonDisplay(SevenSegmentDigit):
  """PunctuationDisplay widget provides a widget for displaying
  punctuation characters. """

  def __init__(self, *args, **kwargs) -> None:
    """Initialize the widget."""
    super().__init__(*args, **kwargs)
    if self.getId() == 'clock':
      self.setFixedSize(12, 64)
    if self.getId() == 'statusBarClock':
      self.setFixedSize(6, 32)

  def customPaint(self, painter: QPainter) -> None:
    """Paint the widget."""
    viewRect = painter.viewport()
    width, height = viewRect.width(), viewRect.height()
    r = height / 16
    yTop = height / 3
    yBottom = height - yTop
    x = width / 2
    painter.setBrush(self.getStyle('highBrush'))
    painter.drawEllipse(QPointF(x, yTop), r, r)
    painter.drawEllipse(QPointF(x, yBottom), r, r)
