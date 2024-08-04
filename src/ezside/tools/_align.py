"""Align provides a KeeNum enumeration of alignments."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TypeAlias, Union, Self

from PySide6.QtCore import QRect, QRectF, QPointF
from worktoy.desc import Field
from worktoy.keenum import KeeNum, auto
from worktoy.text import monoSpace, typeMsg

Rect: TypeAlias = Union[QRect, QRectF]


class Align(KeeNum):
  """Align provides a KeeNum enumeration of alignments."""

  horizontal = Field()
  vertical = Field()

  CENTER = auto()

  LEFT = auto()
  RIGHT = auto()
  TOP = auto()
  BOTTOM = auto()

  TOP_LEFT = auto()
  TOP_RIGHT = auto()
  BOTTOM_RIGHT = auto()
  BOTTOM_LEFT = auto()

  @horizontal.GET
  def _getHorizontal(self) -> Self:
    """Returns True if the alignment is horizontal."""
    if self in [Align.CENTER, Align.TOP, Align.BOTTOM]:
      return Align.Center
    if self in [Align.LEFT, Align.TOP_LEFT, Align.BOTTOM_LEFT]:
      return Align.Left
    if self in [Align.RIGHT, Align.TOP_RIGHT, Align.BOTTOM_RIGHT]:
      return Align.Right

  @vertical.GET
  def _getVertical(self) -> Self:
    """Returns True if the alignment is vertical."""
    if self in [Align.CENTER, Align.LEFT, Align.RIGHT]:
      return Align.Center
    if self in [Align.TOP, Align.TOP_LEFT, Align.TOP_RIGHT]:
      return Align.Top
    if self in [Align.BOTTOM, Align.BOTTOM_LEFT, Align.BOTTOM_RIGHT]:
      return Align.Bottom

  def __add__(self, other: Self) -> Self:
    """Combines horizontal and vertical alignments. """
    if not isinstance(other, Align):
      return super().__add__(other)
    if Align.CENTER not in [self.horizontal, self.vertical]:
      e = """Corner alignments do not support addition, but received: 
      '%s'!""" % self
      raise ValueError(monoSpace(e))
    if Align.CENTER not in [other.horizontal, other.vertical]:
      e = """Corner alignments do not support addition, but received: 
      '%s'!""" % self
      raise ValueError(monoSpace(e))
    if self is Align.CENTER:
      return other
    if other is Align.CENTER:
      return self
    if self is other:
      return self
    if self.horizontal is Align.CENTER and other.horizontal is Align.CENTER:
      e = """Incompatible alignments: '%s' and '%s'!""" % (self, other)
      raise ValueError(monoSpace(e))
    if self.vertical is Align.CENTER and other.vertical is Align.CENTER:
      e = """Incompatible alignments: '%s' and '%s'!""" % (self, other)
      raise ValueError(monoSpace(e))
    if self is Align.LEFT:
      if other is Align.TOP:
        return Align.TOP_LEFT
      if other is Align.BOTTOM:
        return Align.BOTTOM_LEFT
    if self is Align.RIGHT:
      if other is Align.TOP:
        return Align.TOP_RIGHT
      if other is Align.BOTTOM:
        return Align.BOTTOM_RIGHT
    if self is Align.TOP:
      if other is Align.LEFT:
        return Align.TOP_LEFT
      if other is Align.RIGHT:
        return Align.TOP_RIGHT
    if self is Align.BOTTOM:
      if other is Align.LEFT:
        return Align.BOTTOM_LEFT
      if other is Align.RIGHT:
        return Align.BOTTOM_RIGHT

  def fitRect(self, movingRect: Rect, targetRect: Rect) -> Rect:
    """This method receives a moving rectangle and aligns it against a
    target rectangle according to the alignment."""
    movingSize = movingRect.size()
    movingHeight, movingWidth = movingSize.height(), movingSize.width()
    topLeft = targetRect.topLeft()
    targetTop, targetLeft = topLeft.y(), topLeft.x()
    bottomRight = targetRect.bottomRight()
    targetBottom, targetRight = bottomRight.y(), bottomRight.x()
    targetWidth, targetHeight = targetRect.width(), targetRect.height()
    fittedLeft, fittedTop, fittedRight, fittedBottom = None, None, None, None
    #  Horizontal alignment
    if self.horizontal is Align.LEFT:
      fittedLeft = targetLeft
    elif self.horizontal is Align.RIGHT:
      fittedLeft = targetRight - movingWidth
    elif self.horizontal is Align.CENTER:
      fittedLeft = targetLeft + (targetWidth - movingWidth) / 2
    else:
      e = """Unexpected horizontal value received!"""
      raise ValueError(monoSpace(e))
    #  Vertical alignment
    if self.vertical is Align.TOP:
      fittedTop = targetTop
    elif self.vertical is Align.BOTTOM:
      fittedTop = targetBottom - movingHeight
    elif self.vertical is Align.CENTER:
      fittedTop = targetTop + (targetHeight - movingHeight) / 2
    else:
      e = """Unexpected vertical value received!"""
      raise ValueError(monoSpace(e))
    fittedCenterX = fittedLeft + movingWidth / 2
    fittedCenterY = fittedTop + movingHeight / 2
    fittedCenter = QPointF(fittedCenterX, fittedCenterY)
    if isinstance(movingRect, QRect):
      movingRect.moveCenter(fittedCenter.toPoint())
    elif isinstance(movingRect, QRectF):
      movingRect.moveCenter(fittedCenter)
    else:
      e = typeMsg('movingRect', movingRect, QRect)
      raise TypeError(e)
    return movingRect

  def __complex__(self) -> complex:
    """Returns a complex number representing the alignment."""
    a, b = None, None
    h = {Align.LEFT: -1, Align.RIGHT: 1, Align.CENTER: 0}
    v = {Align.TOP: -1, Align.BOTTOM: 1, Align.CENTER: 0}

    return h[self.horizontal] + v[self.vertical] * 1j
