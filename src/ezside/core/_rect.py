"""Rect provides a dataclass representation of a rectangle relative to
some coordinate system. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from typing import Self, TYPE_CHECKING

from PySide6.QtCore import QRect, QRectF, QPoint, QSize
from worktoy.desc import AttriBox, Field, THIS
from worktoy.base import BaseObject, overload

from . import Point, Size, Margin


class Rect(BaseObject):
  """Rect provides a dataclass representation of a rectangle relative to
  some coordinate system. """

  #  Fundamental values
  left = AttriBox[int](0)
  top = AttriBox[int](0)
  right = AttriBox[int](0)
  bottom = AttriBox[int](0)

  #  Derived values
  center = Field()
  topLeft = Field()
  topRight = Field()
  bottomRight = Field()
  bottomLeft = Field()
  size = Field()
  width = Field()
  height = Field()
  Q = Field()

  @Q.GET
  def _getQRect(self) -> QRect:
    L = int(self.left)
    T = int(self.top)
    R = int(self.right)
    B = int(self.bottom)
    topLeft = QPoint(L, T)
    size = QSize(R - L, B - T)
    return QRect(topLeft, size)

  @center.GET
  def _getCenter(self) -> Point:
    x = (self.left + self.right) // 2
    y = (self.top + self.bottom) // 2
    return Point(x, y)

  @topLeft.GET
  def _getTopLeft(self) -> Point:
    return Point(self.left, self.top)

  @topRight.GET
  def _getTopRight(self) -> Point:
    return Point(self.right, self.top)

  @bottomRight.GET
  def _getBottomRight(self) -> Point:
    return Point(self.right, self.bottom)

  @bottomLeft.GET
  def _getBottomLeft(self) -> Point:
    return Point(self.left, self.bottom)

  @size.GET
  def _getSize(self) -> Size:
    w = self.right - self.left
    h = self.bottom - self.top
    return Size(w, h)

  @width.GET
  def _getWidth(self) -> int:
    return int(self.right - self.left)

  @height.GET
  def _getHeight(self) -> int:
    return int(self.bottom - self.top)

  @overload(int, int, int, int)
  def __init__(self, L: int, T: int, R: int, B: int) -> None:
    self.left = L
    self.top = T
    self.right = R
    self.bottom = B

  @overload(int, int, Size)
  def __init__(self, L: int, T: int, S: Size) -> None:
    self.left = L
    self.top = T
    self.right = L + S.width
    self.bottom = T + S.height

  @overload(Point, Size)
  def __init__(self, topLeft: Point, S: Size) -> None:
    self.left = topLeft.x
    self.top = topLeft.y
    self.right = topLeft.x + S.width
    self.bottom = topLeft.y + S.height

  @overload(Point, int, int)
  def __init__(self, topLeft: Point, W: int, H: int) -> None:
    self.left = topLeft.x
    self.top = topLeft.y
    self.right = topLeft.x + W
    self.bottom = topLeft.y + H

  @overload(Point, Point)
  def __init__(self, topLeft: Point, bottomRight: Point) -> None:
    self.left = topLeft.x
    self.top = topLeft.y
    self.right = bottomRight.x
    self.bottom = bottomRight.y

  @overload(Size)
  def __init__(self, size: Size) -> None:
    self.left = 0
    self.top = 0
    self.right = size.width
    self.bottom = size.height

  @overload(THIS)
  def __init__(self, other: Rect) -> None:
    self.left = other.left
    self.top = other.top
    self.right = other.right
    self.bottom = other.bottom

  @overload(QRect)
  def __init__(self, rect: QRect) -> None:
    self.left = rect.left()
    self.top = rect.top()
    self.right = rect.right()
    self.bottom = rect.bottom()

  @overload(QRectF)
  def __init__(self, rect: QRectF) -> None:
    rect = rect.toRect()
    self.left = rect.left()
    self.top = rect.top()
    self.right = rect.right()
    self.bottom = rect.bottom()

  @overload()
  def __init__(self) -> None:
    self.left = 0
    self.top = 0
    self.right = 0
    self.bottom = 0

  @overload(Point)
  def translate(self, point: Point) -> None:
    """Moves this rect by the given point."""
    self.left += point.x
    self.top += point.y
    self.right += point.x
    self.bottom += point.y

  @overload(THIS)
  def translate(self, other: Self) -> None:
    """Moves this rect such that the center of this rect coincides with
    the center of the other rect."""
    if TYPE_CHECKING:
      assert isinstance(other.center, Point)
      assert isinstance(self.center, Point)
      assert callable(self.translate)
    offset = other.center - self.center
    self.translate(offset)

  @overload(Point)
  def translated(self, point: Point) -> Self:
    """Returns a new instance of Rect translated by the given point."""
    cls = type(self)
    L = self.left + point.x
    T = self.top + point.y
    R = self.right + point.x
    B = self.bottom + point.y
    return cls(L, T, R, B)

  @overload(THIS)
  def translated(self, other: Self) -> Self:
    """Returns a new instance of Rect translated by the given rect."""
    cls = type(self)
    L = self.left + other.left
    T = self.top + other.top
    R = self.right + other.right
    B = self.bottom + other.bottom
    return cls(L, T, R, B)

  def __add__(self, other: Margin) -> Self:
    """Adds the given margin to the rectangle."""
    cls = type(self)
    L = self.left - other.left
    T = self.top - other.top
    R = self.right + other.right
    B = self.bottom + other.bottom
    rect = cls(L, T, R, B)
    if TYPE_CHECKING:
      assert callable(rect.translated)
    return rect.translated(other.eccentricity)

  def __iadd__(self, other: Margin) -> Self:
    """Adds the given margin to the rectangle."""
    if TYPE_CHECKING:
      assert callable(self.translate)
    self.left -= other.left
    self.top -= other.top
    self.right += other.right
    self.bottom += other.bottom
    self.translate(other.eccentricity)
    return self

  def __sub__(self, other: Margin) -> Self:
    """Subtracts the given margin from the rectangle."""
    cls = type(self)
    L = self.left + other.left
    T = self.top + other.top
    R = self.right - other.right
    B = self.bottom - other.bottom
    rect = cls(L, T, R, B)
    if TYPE_CHECKING:
      assert callable(rect.translated)
    return rect.translated(-other.eccentricity)

  def __isub__(self, other: Margin) -> Self:
    """Subtracts the given margin from the rectangle."""
    if TYPE_CHECKING:
      assert callable(self.translate)
    self.left += other.left
    self.top += other.top
    self.right -= other.right
    self.bottom -= other.bottom
    self.translate(-other.eccentricity)
    return self

  def __str__(self, ) -> str:
    """String representation of the rectangle."""
    info = """left=%d, top=%d, width=%d, height=%d"""
    return info % (self.left, self.top, self.width, self.height)

  def __repr__(self, ) -> str:
    """String representation of the rectangle."""
    return """<Rect object at %s: %s>""" % (hex(id(self)), str(self))
