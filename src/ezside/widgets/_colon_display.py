"""ColonDisplay displays a colon. Used by digital clock widget. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtCore import Qt, QRectF, QPointF, QSizeF, QMargins
from PySide6.QtGui import QPaintEvent, QPainter, QBrush, QColor

from ezside.core import emptyPen, SolidFill
from ezside.widgets import SevenSegmentDigit


class ColonDisplay(SevenSegmentDigit):
  """PunctuationDisplay widget provides a widget for displaying
  punctuation characters. """

  def __init__(self, *args, **kwargs) -> None:
    """Initialize the widget."""
    super().__init__(*args, **kwargs)
    self.setFixedHeight(32)
    self.setFixedWidth(8)

  @classmethod
  def registerFields(cls) -> dict[str, Any]:
    """Register the fields."""
    return {
      'backgroundColor' : QColor(223, 223, 223),
      'highSegmentColor': QColor(0, 0, 0),
      'lowSegmentColor' : QColor(215, 215, 215),
      'segmentAspect'   : 0.25,
      'segmentSpacing'  : 1,
      'cornerRadius'    : 1,
      'margins'         : QMargins(2, 2, 2, 2, ),
    }

  def paintEvent(self, event: QPaintEvent) -> None:
    """Paint the widget."""
    painter = QPainter()
    painter.begin(self)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    margins = self._getFieldValue('margins')
    viewRect = painter.viewport() - margins
    height = viewRect.height() / 6
    width = viewRect.width()
    topTop = height + margins.top()
    bottomTop = viewRect.height() - 2 * height + margins.top()
    left = margins.left()
    size = QSizeF(width, height)
    top = QRectF(QPointF(left, topTop), size)
    bottom = QRectF(QPointF(left, bottomTop), size)
    brush = QBrush()
    brush.setColor(QColor(0, 0, 0, ))
    brush.setStyle(SolidFill)
    painter.setBrush(brush)
    painter.setPen(emptyPen())
    painter.drawRoundedRect(top, 1, 1)
    painter.drawRoundedRect(bottom, 1, 1)
    painter.end()
