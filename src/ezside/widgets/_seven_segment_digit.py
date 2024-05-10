"""SevenSegmentDigit class for displaying numbers on a 7-segment display."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtCore import QSizeF, QPointF, QRectF, QMargins, QPoint, QSize
from PySide6.QtGui import QPainter, QBrush, QColor, QPen
from PySide6.QtWidgets import QWidget
from icecream import ic
from vistutils.parse import maybe
from vistutils.text import monoSpace
from vistutils.waitaminute import typeMsg

from ezside.core import SolidFill, \
  SolidLine, \
  Expand, \
  AlignHCenter, \
  AlignVCenter
from ezside.widgets import BaseWidget, CanvasWidget

ic.configureOutput(includeContext=True, )


class SevenSegmentDigit(CanvasWidget):
  """SevenSegment class for displaying numbers on a 7-segment display."""

  __inner_value__ = None
  __power_scale__ = None
  __inner_scale__ = None
  __is_dot__ = None

  def __init__(self, *args, **kwargs) -> None:
    self.__power_scale__ = kwargs.get('scale', 1)
    parent, scale = None, kwargs.get('scale', None)
    for arg in args:
      if isinstance(arg, QWidget) and parent is None:
        parent = arg
      elif isinstance(arg, int) and scale is None:
        power = arg
      if parent is not None and scale is not None:
        break
    else:
      self.__power_scale__ = maybe(scale, 1)
    CanvasWidget.__init__(self, *args, **kwargs)
    self.__is_dot__ = kwargs.get('dot', False)
    self.setMinimumSize(QSize(48, 96))

  def initUi(self, ) -> None:
    """Initialize the user interface."""

  def initSignalSlot(self) -> None:
    """Initialize the signal slot."""

  @classmethod
  def registerFields(cls) -> dict[str, Any]:
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
      'radius'         : QPoint(2, 2, ),
      'vAlign'         : AlignVCenter,
      'hAlign'         : AlignHCenter,
      'aspect'         : 0.25,
      'spacing'        : 2,
    }

  @classmethod
  def registerStates(cls) -> list[str]:
    """Register the states."""
    return ['base', ]

  @classmethod
  def registerDynamicFields(cls) -> dict[str, Any]:
    """Implementation of dynamic fields"""
    highBrush = QBrush()
    highBrush.setStyle(SolidFill)
    highBrush.setColor(QColor(144, 255, 0))
    lowBrush = QBrush()
    lowBrush.setStyle(SolidFill)
    lowBrush.setColor(QColor(0, 0, 15))
    return {
      'backgroundColor': QColor(15, 0, 0),
      'highBrush'      : highBrush,
      'lowBrush'       : lowBrush,
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

  def increment(self) -> None:
    """Increments the inner value rolling over from 9 to 0"""
    self.update()
    self._setInnerValue((self._getInnerValue() + 1) % 10)

  def decrement(self) -> None:
    """Decrements the inner value rolling over from 0 to 9"""
    self.update()
    self._setInnerValue((self._getInnerValue() - 1) % 10)

  def _getSegState(self, segment: str) -> bool:
    """Get the segment state."""
    return True if segment in self.map7()[int(self)] else False

  def __int__(self, ) -> int:
    """Returns the inner value."""
    return self._getInnerValue()

  @staticmethod
  def map7() -> list[list[str]]:
    """This method returns a list of lists of strings, where at each index
    of the outer list, there is a list of strings representing the segments
    that should be on for the corresponding digit. """
    return [
      ['A', 'B', 'C', 'D', 'E', 'F'],
      ['B', 'C'],
      ['A', 'B', 'G', 'E', 'D'],
      ['A', 'B', 'G', 'C', 'D'],
      ['F', 'G', 'B', 'C'],
      ['A', 'F', 'G', 'C', 'D'],
      ['A', 'F', 'G', 'C', 'D', 'E'],
      ['A', 'B', 'C'],
      ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
      ['A', 'B', 'C', 'D', 'F', 'G'],
    ]

  def map7seg(self) -> list[str]:
    """This method returns a list of strings representing the segments that
    should be on for the corresponding digit. """
    return self.map7()[int(self)]

  def _getSegPen(self, segment: str) -> QPen:
    """Get the pen."""
    if self._getSegState(segment):
      return self.getStyle('highPen')
    return self.getStyle('lowPen')

  def _getSegBrush(self, segment: str) -> QBrush:
    """Get the segment brush."""
    if self._getSegState(segment):
      return self.getStyle('highBrush')
    return self.getStyle('lowBrush')

  def getScale(self) -> int:
    """Public getter for the power scale."""
    return self.__inner_scale__

  def __float__(self) -> float:
    """Returns the inner value multiplied by 10 to the power at power
    scale. Please note that this may be negative. """
    return float(self._getInnerValue() * self.getScale())

  def customPaint(self, painter: QPainter) -> None:
    """Custom paint method for Label."""
    viewRect = painter.viewport()
    width, height = viewRect.width(), viewRect.height()
    spacing = self.getStyle('spacing')
    aspect = 0.25
    segmentWidth = (width - 4 * spacing) / (1 + 2 * aspect)
    segmentHeight = aspect * segmentWidth
    hSize = QSizeF(segmentWidth, segmentHeight)
    vSize = QSizeF(segmentHeight, segmentWidth)
    EFLeft = spacing
    ADGLeft = 2 * spacing + segmentHeight
    BCLeft = ADGLeft + segmentWidth + spacing
    ATop = 0
    BFTop = spacing + segmentHeight
    CETop = BFTop + segmentWidth + 2 * spacing + segmentHeight
    DTop = CETop + segmentWidth + spacing
    GTop = ATop / 2 + DTop / 2
    topSpace = spacing
    bottomSpace = height - GTop + segmentHeight
    avgSpace = 0.5 * (topSpace + bottomSpace) - topSpace
    offSet = (height - DTop - segmentHeight) / 2

    segments = {
      'A': QRectF(QPointF(ADGLeft, ATop + offSet), hSize),
      'B': QRectF(QPointF(BCLeft, BFTop + offSet), vSize),
      'C': QRectF(QPointF(BCLeft, CETop + offSet), vSize),
      'D': QRectF(QPointF(ADGLeft, DTop + offSet), hSize),
      'E': QRectF(QPointF(EFLeft, CETop + offSet), vSize),
      'F': QRectF(QPointF(EFLeft, BFTop + offSet), vSize),
      'G': QRectF(QPointF(ADGLeft, GTop + offSet), hSize),
    }
    highSegments = []
    lowSegments = []
    high7 = self.map7seg()
    for (seg, rect) in segments.items():
      if seg in high7:
        highSegments.append(rect)
      else:
        lowSegments.append(rect)
    painter.setBrush(self.getStyle('lowBrush'))
    painter.setPen(self.getStyle('lowPen'))
    for rect in lowSegments:
      painter.drawRect(rect)
    painter.setBrush(self.getStyle('highBrush'))
    painter.setPen(self.getStyle('highPen'))
    for rect in highSegments:
      painter.drawRect(rect)
