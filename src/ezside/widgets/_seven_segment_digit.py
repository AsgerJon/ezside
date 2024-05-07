"""SevenSegmentDigit class for displaying numbers on a 7-segment display."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtCore import QSizeF, QPointF, QRectF, QSize
from PySide6.QtGui import QPaintEvent, QPainter, QBrush, QColor, QPen
from PySide6.QtWidgets import QWidget
from vistutils.text import monoSpace
from vistutils.waitaminute import typeMsg

from ezside.core import SolidFill, emptyPen, SolidLine, Tight
from ezside.widgets import BaseWidget


class SevenSegmentDigit(BaseWidget):
  """SevenSegment class for displaying numbers on a 7-segment display."""

  __inner_value__ = None
  __power_scale__ = None
  __is_dot__ = None

  def __init__(self, *args, **kwargs) -> None:
    parent, power = None, kwargs.get('scale', None)
    for arg in args:
      if isinstance(arg, QWidget) and parent is None:
        parent = arg
      elif isinstance(arg, int) and power is None:
        power = arg
      if parent is not None and power is not None:
        break
    else:
      power = 4 if power is None else power
    self.__power_scale__ = power
    BaseWidget.__init__(self, parent)
    self.setMinimumSize(QSize(32, 64))
    self.setSizePolicy(Tight, Tight)

  @classmethod
  def registerFields(cls) -> dict[str, Any]:
    """Register the fields."""
    return {
      'backgroundColor' : QColor(223, 223, 223),
      'highSegmentColor': QColor(0, 0, 0),
      'lowSegmentColor' : QColor(191, 191, 191),
      'segmentAspect'   : 0.2,
      'segmentSpacing'  : 4,
      'cornerRadius'    : 2
    }

  def _getInnerValue(self) -> int:
    """Get the inner value."""
    self.update()
    if self.__inner_value__ is None:
      return 0
    if isinstance(self.__inner_value__, int):
      if abs(self.__inner_value__) > 9:
        e = """Each digit supports no higher than 9, but received: %d"""
        raise ValueError(monoSpace(e % self.__inner_value__))
      return abs(self.__inner_value__)
    e = typeMsg('inner_value', self.__inner_value__, int)
    raise TypeError(e)

  def _setInnerValue(self, value: int) -> None:
    """Set the inner value."""
    self.update()
    if isinstance(value, int):
      if abs(value) > 9:
        e = """Each digit supports no higher than 9, but received: %d"""
        raise ValueError(monoSpace(e % value))
      self.__inner_value__ = abs(value)
    else:
      e = typeMsg('value', value, int)
      raise TypeError(e)

  def _increment(self) -> None:
    """Increments the inner value rolling over from 9 to 0"""
    self.update()
    self._setInnerValue((self._getInnerValue() + 1) % 10)

  def _decrement(self) -> None:
    """Decrements the inner value rolling over from 0 to 9"""
    self.update()
    self._setInnerValue((self._getInnerValue() - 1) % 10)

  def _getSegState(self, segment: str) -> bool:
    """Get the segment state."""
    if not isinstance(segment, str):
      e = typeMsg('segment', segment, str)
      raise TypeError(e)
    if segment not in 'ABCDEFG' + 'abcdefg':
      e = """The segment must be one of 'ABCDEFG', but received: %s"""
      raise ValueError(monoSpace(e % segment))
    value = self._getInnerValue()
    if segment == 'A':
      return True if value in [0, 2, 3, 5, 6, 7, 8, 9] else False
    if segment == 'B':
      return True if value in [0, 1, 2, 3, 4, 7, 8, 9] else False
    if segment == 'C':
      return True if value in [0, 1, 3, 4, 5, 6, 7, 8, 9] else False
    if segment == 'D':
      return True if value in [0, 2, 3, 5, 6, 8, 9] else False
    if segment == 'E':
      return True if value in [0, 2, 6, 8] else False
    if segment == 'F':
      return True if value in [0, 4, 5, 6, 8, 9] else False
    if segment == 'G':
      return True if value in [2, 3, 4, 5, 6, 8, 9] else False
    raise ValueError(monoSpace('The segment must be one of "ABCDEFG"'))

  def _getSegBrush(self, segment: str) -> QBrush:
    """Get the segment brush."""
    if not isinstance(segment, str):
      e = typeMsg('segment', segment, str)
      raise TypeError(e)
    if segment not in 'ABCDEFG' + 'abcdefg':
      e = """The segment must be one of 'ABCDEFG', but received: %s"""
      raise ValueError(monoSpace(e % segment))
    high = self._getFieldValue('highSegmentColor')
    low = self._getFieldValue('lowSegmentColor')
    brush = QBrush()
    brush.setStyle(SolidFill)
    brush.setColor(high if self._getSegState(segment) else low)
    return brush

  def _getSegPen(self, segment: str) -> QPen:
    """Get the segment pen."""
    if not isinstance(segment, str):
      e = typeMsg('segment', segment, str)
      raise TypeError(e)
    if segment not in 'ABCDEFG' + 'abcdefg':
      e = """The segment must be one of 'ABCDEFG', but received: %s"""
      raise ValueError(monoSpace(e % segment))
    pen = QPen()
    pen.setStyle(SolidLine)
    pen.setWidth(1)
    pen.setColor(QColor(0, 0, 0, ))
    return emptyPen() if self._getSegState(segment) else pen

  def _setPowerScale(self, scale: int) -> None:
    """Set the power scale."""
    self.__power_scale__ = scale

  def _getPowerScale(self) -> int:
    """Get the power scale."""
    return self.__power_scale__

  def getScale(self) -> int:
    """Public getter for the power scale."""
    return self._getPowerScale()

  def _incPowerScale(self) -> None:
    """Increment the power scale."""
    self.__power_scale__ += 1

  def _decPowerScale(self) -> None:
    """Decrement the power scale."""
    self.__power_scale__ -= 1

  def dotLeft(self, ) -> None:
    """Set the dot to the left."""
    if self.__is_dot__:
      self.__is_dot__ = False
      self.__power_scale__ = -1
    elif not self.__power_scale__:
      self.__is_dot__ = True
    else:
      self.__power_scale__ -= 1

  def dotRight(self, ) -> None:
    """Set the dot to the right."""
    if self.__is_dot__:
      self.__is_dot__ = False
      self.__power_scale__ = 0
    elif not self.__power_scale__:
      self.__is_dot__ = True
    else:
      self.__power_scale__ += 1

  def __float__(self) -> float:
    """Returns the inner value multiplied by 10 to the power at power
    scale. Please note that this may be negative. """
    return self._getInnerValue() * 10 ** self._getPowerScale()

  def paintEvent(self, event: QPaintEvent) -> None:
    """Custom implementation of paint event"""
    aspect = self._getFieldValue('segmentAspect')
    radius = self._getFieldValue('cornerRadius')
    spacing = self._getFieldValue('segmentSpacing')
    painter = QPainter()
    painter.begin(self)
    painter.setPen(emptyPen())
    viewRect = painter.viewport()
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    H, W = viewRect.height(), viewRect.width()
    if self.__is_dot__:
      color = self._getFieldValue('highSegmentColor')
      brush = QBrush()
      brush.setStyle(SolidFill)
      brush.setColor(color)
      painter.setBrush(brush)
      dotR = viewRect.width() / 3
      dotX = viewRect.center().x()
      dotY = viewRect.bottom() - dotR * 1.5
      center = QPointF(dotX, dotY)
      painter.drawEllipse(center, dotR, dotR)
    else:
      w = (W - 4 * spacing) / (1 + 2 * aspect)
      h = aspect * w
      hSize = QSizeF(w, h)
      vSize = QSizeF(h, w)
      ATop = spacing
      BFTop = 2 * spacing + h
      CETop = BFTop + w + 2 * spacing + h
      DTop = CETop + w + spacing
      GTop = ATop / 2 + DTop / 2
      FLeft = spacing
      ELeft = spacing
      GLeft = 2 * spacing + h
      ALeft = GLeft
      DLeft = GLeft
      BLeft = ALeft + w + spacing
      CLeft = BLeft
      A = QPointF(ALeft, ATop)
      B = QPointF(BLeft, BFTop)
      C = QPointF(CLeft, CETop)
      D = QPointF(DLeft, DTop)
      E = QPointF(ELeft, CETop)
      F = QPointF(FLeft, BFTop)
      G = QPointF(GLeft, GTop)
      segments = {
        'A': QRectF(A, hSize),
        'B': QRectF(B, vSize),
        'C': QRectF(C, vSize),
        'D': QRectF(D, hSize),
        'E': QRectF(E, vSize),
        'F': QRectF(F, vSize),
        'G': QRectF(G, hSize),
      }
      for (seg, rect) in segments.items():
        painter.setBrush(self._getSegBrush(seg))
        painter.setPen(self._getSegPen(seg))
        painter.drawRoundedRect(rect, radius, radius)
    debugBrush = QBrush()
    debugBrush.setStyle(SolidFill)
    coin = self._getPowerScale() % 2
    color = QColor(255, 0, 144, 63) if coin else QColor(144, 255, 0, 63)
    debugBrush.setColor(color)
    painter.setBrush(debugBrush)
    lmaoRect = QRectF(QPointF(0, 0), QSize(W, H))
    painter.drawRect(lmaoRect)
    painter.end()
