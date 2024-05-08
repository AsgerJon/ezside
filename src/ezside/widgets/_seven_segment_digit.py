"""SevenSegmentDigit class for displaying numbers on a 7-segment display."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtCore import QSizeF, QPointF, QRectF, QMargins
from PySide6.QtGui import QPaintEvent, QPainter, QBrush, QColor, QPen
from PySide6.QtWidgets import QWidget
from icecream import ic
from vistutils.text import monoSpace
from vistutils.waitaminute import typeMsg

from ezside.core import SolidFill, emptyPen, SolidLine, Expand
from ezside.widgets import BaseWidget

ic.configureOutput(includeContext=True, )


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
    BaseWidget.__init__(self, *args, **kwargs)
    self.__is_dot__ = kwargs.get('dot', False)

  def initUi(self, ) -> None:
    """Initialize the user interface."""
    self.setFixedHeight(32)
    self.setFixedWidth(16)
    self.setSizePolicy(Expand, Expand)

  def initSignalSlot(self) -> None:
    """Initialize the signal slot."""

  @classmethod
  def registerFields(cls) -> dict[str, Any]:
    """Register the fields."""
    backgroundBrush = QBrush()
    backgroundBrush.setStyle(SolidFill)
    backgroundBrush.setColor(QColor(223, 223, 223))
    backgroundPen = QPen()
    backgroundPen.setStyle(SolidLine)
    backgroundPen.setWidth(1)
    backgroundPen.setColor(QColor(0, 0, 0, 0))
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
      'backgroundBrush' : 777777777,
      'backgroundBorder': QColor(0, 0, 0, 0),
      'backgroundFill'  : QColor(223, 223, 223),
      'backgroundWidth' : 1,
      'highFill'        : QColor(0, 0, 0),
      'lowFill'         : QColor(215, 215, 215),
      'highWidth'       : 0,
      'lowWidth'        : 0,
      'highBorder'      : QColor(191, 191, 191),
      'lowBorder'       : QColor(191, 191, 191),
      'aspect'          : 0.25,
      'spacing'         : 1,
      'radius'          : 1,
      'margins'         : QMargins(0, 0, 0, 0, ),
    }

  @classmethod
  def registerStates(cls) -> list[str]:
    """Register the states."""
    return ['base', ]

  @classmethod
  def registerDynamicFields(cls) -> dict[str, Any]:
    """Implementation of dynamic fields"""
    return {
      '%s/clock/base/backgroundFill' % cls.__name__: QColor(15, 0, 0),
      '%s/clock/base/highColor' % cls.__name__     : QColor(144, 255, 0),
      '%s/clock/base/lowColor' % cls.__name__      : QColor(0, 0, 15),
    }

  def detectState(self, ) -> str:
    """Detect the state."""
    return 'base'

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

  def setInnerValue(self, value: int) -> None:
    """Public setter for the inner value."""
    self._setInnerValue(value)

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

  def _getLowPen(self) -> QPen:
    """Get the low pen."""
    pen = QPen()
    pen.setStyle(SolidLine)
    pen.setWidth(self._getStyle('lowWidth'))
    pen.setColor(self._getStyle('lowBorder'))
    return pen

  def _getHighPen(self) -> QPen:
    """Get the high pen."""
    pen = QPen()
    pen.setStyle(SolidLine)
    pen.setWidth(self._getStyle('highWidth'))
    pen.setColor(self._getStyle('highBorder'))
    return pen

  def _getSegPen(self, segment: str) -> QPen:
    """Get the pen."""
    if self._getSegState(segment):
      return self._getHighPen()
    return self._getLowPen()

  def _getLowBrush(self) -> QBrush:
    """Get the low brush."""
    brush = QBrush()
    brush.setStyle(SolidFill)
    brush.setColor(self._getStyle('lowFill'))
    return brush

  def _getHighBrush(self) -> QBrush:
    """Get the high brush."""
    brush = QBrush()
    brush.setStyle(SolidFill)
    brush.setColor(self._getStyle('highFill'))
    return brush

  def _getSegBrush(self, segment: str) -> QBrush:
    """Get the segment brush."""
    if self._getSegState(segment):
      return self._getHighBrush()
    return self._getLowBrush()

  def _getBackgroundBrush(self) -> QBrush:
    """Get the background brush."""
    brush = QBrush()
    brush.setStyle(SolidFill)
    brush.setColor(self._getStyle('backgroundFill'))
    return brush

  def _getBackgroundPen(self) -> QPen:
    """Get the background pen."""
    pen = QPen()
    pen.setStyle(SolidLine)
    width = self._getStyle('backgroundWidth')
    pen.setWidth(self._getStyle('backgroundWidth'))
    pen.setColor(self._getStyle('backgroundBorder'))
    return pen

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
    return float(self._getInnerValue() * 10 ** self._getPowerScale())

  def paintEvent(self, event: QPaintEvent) -> None:
    """Custom implementation of paint event"""
    aspect = self._getStyle('aspect')
    radius = self._getStyle('radius')
    spacing = self._getStyle('spacing')
    margins = self._getStyle('margins')
    painter = QPainter()
    painter.begin(self)
    painter.setPen(emptyPen())
    viewRect = painter.viewport()
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setBrush(self._getBackgroundBrush())
    painter.setPen(self._getBackgroundPen())
    painter.drawRoundedRect(viewRect, radius, radius, )
    innerRect = viewRect - margins
    topMargin, leftMargin = margins.top(), margins.left()
    H, W = innerRect.height(), innerRect.width()
    if self.__is_dot__:
      painter.setBrush(self._getHighBrush())
      dotR = viewRect.width() / 9
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
      bottom = DTop + h + spacing
      dv = (H - bottom) / 2
      A = QPointF(ALeft + leftMargin, ATop + topMargin + dv)
      B = QPointF(BLeft + leftMargin, BFTop + topMargin + dv)
      C = QPointF(CLeft + leftMargin, CETop + topMargin + dv)
      D = QPointF(DLeft + leftMargin, DTop + topMargin + dv)
      E = QPointF(ELeft + leftMargin, CETop + topMargin + dv)
      F = QPointF(FLeft + leftMargin, BFTop + topMargin + dv)
      G = QPointF(GLeft + leftMargin, GTop + topMargin + dv)
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
        painter.drawRect(rect, )
    painter.end()

  BaseWidget.addStyleId('clock')
