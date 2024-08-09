"""SevenSeg provides a widget representation of a seven segment display."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TypeAlias, Union, Self

from PySide6.QtCore import QSize, QSizeF, QPoint, QPointF, QRect, QRectF, \
  QMarginsF
from PySide6.QtGui import QPaintEvent, QPainter, QColor, QPen, QBrush
from icecream import ic
from worktoy.desc import AttriBox, Field
from worktoy.keenum import KeeNum, auto
from worktoy.parse import maybe

from ezside.tools import emptyBrush, parsePen, fillBrush, emptyPen
from ezside.basewidgets import BoxWidget

Size: TypeAlias = Union[QSize, QSizeF]
Point: TypeAlias = Union[QPoint, QPointF]

ic.configureOutput(includeContext=True)


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

  scale = AttriBox[float](0.12)
  segmentMargins = AttriBox[QMarginsF](QMarginsF(0, 0, 0, 0))
  highMargins = AttriBox[QMarginsF](QMarginsF(1, 1, 1, 1, ) * 0.2)
  lowMargins = AttriBox[QMarginsF](QMarginsF(1, 1, 1, 1, ) * 0.2)
  highColor = AttriBox[QColor](QColor(255, 0, 0, 255))
  lowColor = AttriBox[QColor](QColor(0, 0, 0, 255))

  aspectRect = Field()
  digit = Field()
  segmentPen = Field()
  highBrush = Field()
  lowBrush = Field()

  def __init__(self, *args) -> None:
    BoxWidget.__init__(self, *args)
    self.backgroundColor = QColor(63, 0, 0, 255)

  def requiredSize(self) -> QSizeF:
    """This method returns the required size of the widget."""
    return self.requiredRect().size()

  def requiredRect(self) -> QRectF:
    """This method returns the required rectangle of the widget."""
    return QRectF(QPointF(0, 0), QSizeF(24, 32))

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
    if isinstance(offSet, QPointF):
      return self._getRects(size, QPointF.toPoint(offSet))
    if isinstance(size, QSizeF):
      return self._getRects(QSizeF.toSize(size), offSet)
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
      size = QRectF(origin, size).marginsRemoved(self.segmentMargins).size()
      h, w = size.height(), size.width()
      if size.width() < 2:
        h, w = 2 * size.height() / size.width(), 2
        size = QSizeF(w, h)
      if size.height() < 2:
        h, w = 2, 2 * size.width() / size.height()
        size = QSizeF(w, h)
      rect = QRectF(origin, size)
      rect.moveCenter(place)
      rects[segment] = QRectF.toRect(rect)
    return rects

  def paintMeLike(self, rect: QRectF, painter: QPainter) -> None:
    """This method allows the layout to paint this widget. """
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    viewRect = rect
    center = viewRect.center()
    marginRect = QRectF.marginsRemoved(viewRect, self.margins)
    borderRect = QRectF.marginsRemoved(marginRect, self.borders)
    paddedRect = QRectF.marginsRemoved(borderRect, self.paddings)
    marginRect.moveCenter(center)
    borderRect.moveCenter(center)
    paddedRect.moveCenter(center)
    #  Draw padded area
    painter.setBrush(self.backgroundBrush)
    painter.setPen(emptyPen())
    painter.drawRect(paddedRect)
    rects = self.getRects(paddedRect)
    for segment, rect in rects.items():
      if segment.state(self.digit):
        painter.setBrush(self.highBrush)
        rect = QRect.toRectF(rect) + self.highMargins
      else:
        painter.setBrush(self.lowBrush)
        rect = QRect.toRectF(rect)
      painter.drawRect(rect)
