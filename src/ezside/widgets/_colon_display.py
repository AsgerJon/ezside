"""ColonDisplay displays a colon. Used by digital clock widget. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtCore import QPointF, QMargins, QPoint
from PySide6.QtGui import QPainter, QBrush, QColor, QPen
from icecream import ic

from ezside.core import SolidFill, SolidLine, AlignHCenter, AlignVCenter
from ezside.widgets import SevenSegmentDigit

ic.configureOutput(includeContext=True, )


class ColonDisplay(SevenSegmentDigit):
  """PunctuationDisplay widget provides a widget for displaying
  punctuation characters. """

  def __init__(self, *args, **kwargs) -> None:
    """Initialize the widget."""
    super().__init__(*args, **kwargs)
    self.setFixedSize(12, 64)

  @classmethod
  def staticStyles(cls) -> dict[str, Any]:
    """Register the fields."""
    highBrush = QBrush()
    highBrush.setStyle(SolidFill)
    highBrush.setColor(QColor(0, 0, 0))
    lowBrush = QBrush()
    lowBrush.setStyle(SolidFill)
    lowBrush.setColor(QColor(215, 215, 215))
    highPen = QPen()
    highPen.setStyle(SolidLine)
    highPen.setWidth(0)
    highPen.setColor(QColor(191, 191, 191))
    lowPen = QPen()
    lowPen.setStyle(SolidLine)
    lowPen.setWidth(0)
    lowPen.setColor(QColor(191, 191, 191))

    return {
      'highBrush'      : highBrush,
      'lowBrush'       : lowBrush,
      'highPen'        : highPen,
      'lowPen'         : lowPen,
      'margins'        : QMargins(2, 2, 2, 2, ),
      'borders'        : QMargins(2, 2, 2, 2, ),
      'paddings'       : QMargins(2, 2, 2, 2, ),
      'borderColor'    : QColor(0, 0, 0, 255),
      'backgroundColor': QColor(223, 223, 223, 255),
      'radius'         : QPoint(0, 0, ),
      'vAlign'         : AlignVCenter,
      'hAlign'         : AlignHCenter,
      'aspect'         : 0.25,
      'spacing'        : 0,
    }

  @classmethod
  def registerStates(cls) -> list[str]:
    """Register the states."""
    return ['base', ]

  def dynStyles(self) -> dict[str, Any]:
    """Implementation of dynamic fields"""
    if self.getId() == 'clock':
      return {
        'margins'        : QMargins(0, 0, 0, 0, ),
        'borders'        : QMargins(0, 2, 0, 2, ),
        'paddings'       : QMargins(0, 0, 0, 0, ),
        'borderColor'    : QColor(0, 0, 0, 255),
        'backgroundColor': QColor(223, 223, 223, 255),
        'radius'         : QPoint(0, 0),
        'vAlign'         : AlignVCenter,
        'hAlign'         : AlignHCenter,
      }

  @classmethod
  def registerStyleIds(cls) -> list[str]:
    """Registers the supported style IDs for Label."""
    return ['normal', ]

  def detectState(self) -> str:
    """Detect the state."""
    return 'base'

  def getStyle(self, name: str) -> Any:
    """Get the style."""
    return super().getStyle(name)

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
