"""SevenSeg provides a widget representation of a seven segment display."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TypeAlias, Union, Self

from PySide6.QtCore import QSize, QSizeF, QPoint, QPointF, QRect, QRectF, \
  QMarginsF
from PySide6.QtGui import QPaintEvent, QPainter, QColor, QPen, QBrush
from worktoy.desc import AttriBox, Field
from worktoy.keenum import KeeNum, auto
from worktoy.parse import maybe

from ezside.tools import emptyBrush, parsePen, fillBrush
from ezside.widgets import BoxWidget

Size: TypeAlias = Union[QSize, QSizeF]
Point: TypeAlias = Union[QPoint, QPointF]


class Segment(KeeNum):
  """Segment provides an enumeration of the seven segments of a seven
  segment display."""

  horizontal = Field()
  vertical = Field()

  A = auto(0, 2, 3, 5, 6, 7, 8, 9)
  B = auto(0, 1, 2, 3, 4, 7, 8, 9)
  C = auto(0, 1, 3, 4, 5, 6, 7, 8, 9)
  D = auto(0, 2, 3, 5, 6, 8, 9)
  E = auto(0, 2, 6, 8)
  F = auto(0, 4, 5, 6, 8, 9)
  G = auto(2, 3, 4, 5, 6, 8, 9)

  @classmethod
  def getHorizontals(cls) -> list[Self]:
    """Getter-function for the horizontal segments."""
    return [cls.A, cls.D, cls.G]

  @classmethod
  def getVerticals(cls) -> list[Self]:
    """Getter-function for the vertical segments."""
    return [cls.B, cls.C, cls.E, cls.F]

  def state(self, digit: int) -> bool:
    """Determines the state of the segment given the digit to be
    displayed."""
    return True if digit in self.value else False

  def aspect(self, ) -> tuple[int, int]:
    """Returns the aspect ratio of the segment"""
    if self in [Segment.A, Segment.D, Segment.G]:
      return 4, 1
    return 1, 6

  @horizontal.GET
  def _getHorizontal(self) -> bool:
    """Returns True if the segment is horizontal."""
    return True if self in self.getHorizontals() else False

  @vertical.GET
  def _getVertical(self) -> bool:
    """Returns True if the segment is vertical."""
    return True if self in self.getVerticals() else False


SegPlace: TypeAlias = dict[Segment, QPoint]
SegSize: TypeAlias = dict[Segment, QSize]
SegRect: TypeAlias = dict[Segment, QRect]


class SevenSeg(BoxWidget):
  """SevenSeg provides a widget representation of a seven segment display."""

  __fallback_digit__ = 0
  __current_digit__ = None

  scale = AttriBox[float](0.1)
  segmentMargins = AttriBox[QMarginsF](QMarginsF(0.25, 0.25, 0.25, 0.25))
  highColor = AttriBox[QColor](QColor(255, 0, 0, 255))
  lowColor = AttriBox[QColor](QColor(127, 0, 0, 255))
  aspectRatio = AttriBox[float](1.5)

  aspectRect = Field()
  digit = Field()
  segmentPen = Field()
  highBrush = Field()
  lowBrush = Field()

  def __init__(self, ) -> None:
    BoxWidget.__init__(self)
    self.setFixedSize(32, 24)

  def minimumSizeHint(self) -> QSize:
    """This method returns the size hint of the widget."""
    return QSize(32, 24)

  @aspectRect.GET
  def _getAspectRect(self) -> QRect:
    """This method returns the aspect ratio of the widget."""
    width, height = self.contentRect.width(), self.contentRect.height()
    if height > width * self.aspectRatio:
      height = width * self.aspectRatio
    if width > height / self.aspectRatio:
      width = height / self.aspectRatio
    rect = QRectF(QPointF(0, 0), QSizeF(width, height))
    return QRectF.toRect(rect)

  @digit.GET
  def _getDigit(self) -> int:
    """Getter-function for current digit"""
    return maybe(self.__current_digit__, self.__fallback_digit__)

  @digit.SET
  def _setDigit(self, digit: int) -> None:
    """Setter-function for current digit"""
    if not isinstance(digit, int):
      e = """Digit must be an integer!"""
      raise TypeError(e)
    if digit < 0 or digit > 9:
      e = """Digit must be between 0 and 9!"""
      raise ValueError(e)
    self.__current_digit__ = digit

  @segmentPen.GET
  def _getSegmentPen(self) -> QPen:
    """This method returns the pen used to paint the segments. """
    return parsePen(2, QColor(0, 0, 0, 255))

  @highBrush.GET
  def _getHighBrush(self) -> QBrush:
    """This method returns the brush used to paint the high segments. """
    return fillBrush(self.highColor)

  @lowBrush.GET
  def _getLowBrush(self) -> QBrush:
    """This method returns the brush used to paint the low segments. """
    return fillBrush(self.lowColor)

  def getRects(self, *args) -> SegRect:
    """Returns the center of each segment."""
    size, offSet = None, None
    for arg in args:
      if isinstance(arg, QRectF):
        return self.getRects(QRectF.toRect(arg))
      if isinstance(arg, QRect):
        return self._getRects(QRect.size(arg), QRect.topLeft(arg))
      if isinstance(arg, QSizeF) and size is None:
        size = QSizeF.toSize(arg)
      if isinstance(arg, QSize) and size is None:
        size = arg
      if isinstance(arg, QPointF) and offSet is None:
        offSet = QPointF.toPoint(arg)
      if isinstance(arg, QPoint) and offSet is None:
        offSet = arg
      if size is not None and offSet is not None:
        return self._getRects(size, offSet)
    else:
      if size is None:
        e = """Unable to parse size!"""
        raise ValueError(e)
      offSet = maybe(offSet, QPoint(0, 0))
      return self._getRects(size, offSet)

  def _getRects(self, size: Size, offSet: Point = None) -> SegRect:
    """Returns the center of each segment."""
    if offSet is None:
      return self._getRects(size, QPoint(0, 0))
    if isinstance(size, QSizeF):
      return self._getRects(QSizeF.toSize(size), QPointF.toPoint(offSet))
    H, W = size.height(), size.width()
    hScale = H / W * self.scale
    vScale = self.scale
    horWidth = W * (1 - 2 * hScale)
    horHeight = H * vScale
    verWidth = W * hScale
    verHeight = H * (1 - 3 * vScale) / 2
    hSize = QSizeF(horWidth, horHeight)
    vSize = QSizeF(verWidth, verHeight)
    out = {}
    centers = {}
    sizes = {}
    rects = {}
    x0, y0 = offSet.x(), offSet.y()
    for segment in Segment:
      sizes[segment] = hSize if segment.horizontal else vSize
    left = verWidth / 2
    right = W - verWidth / 2
    hMid = W / 2
    top = horHeight / 2
    bottom = H - horHeight / 2
    up = horHeight + verHeight / 2
    down = H - horHeight - verHeight / 2
    centers[Segment.A] = QPointF(hMid + x0, top + y0)
    centers[Segment.B] = QPointF(right + x0, up + y0)
    centers[Segment.C] = QPointF(right + x0, down + y0)
    centers[Segment.D] = QPointF(hMid + x0, bottom + y0)
    centers[Segment.E] = QPointF(left + x0, down + y0)
    centers[Segment.F] = QPointF(left + x0, up + y0)
    centers[Segment.G] = QPointF(hMid + x0, H / 2 + y0)
    origin = QPointF(0, 0)
    for segment in Segment:
      place = centers[segment]
      size = sizes[segment]
      rect = QRectF(origin, size).marginsRemoved(self.segmentMargins)
      rect.moveCenter(place)
      rects[segment] = QRectF.toRect(rect)
    return rects

  def paintEvent(self, event: QPaintEvent) -> None:
    """This method handles painting of the widget"""
    BoxWidget.paintEvent(self, event)
    painter = QPainter()
    painter.begin(self)
    #  Draw padded area
    painter.setBrush(emptyBrush())
    painter.setPen(self.segmentPen)
    #  Draw the outline of every segment regardless of state
    rects = self.getRects(self.contentRect)
    for segment, rect in rects.items():
      if segment.state(self.digit):
        painter.setBrush(self.highBrush)
      else:
        painter.setBrush(self.lowBrush)
      painter.drawRoundedRect(rect, 5, 5)
    painter.end()
