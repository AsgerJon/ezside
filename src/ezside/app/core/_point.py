"""Point provides a dataclass representation of a point relative to some
coordinate system."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Self, TYPE_CHECKING

from PySide6.QtCore import QPoint, QPointF
from PySide6.QtGui import QMouseEvent
from worktoy.desc import AttriBox, THIS, Field
from worktoy.base import BaseObject, overload


class Point(BaseObject):
  """Point provides a dataclass representation of a point relative to some
  coordinate system."""

  x = AttriBox[int](0)
  y = AttriBox[int](0)

  Q = Field()

  @Q.GET
  def _getQPoint(self) -> QPoint:
    return QPoint(self.x, self.y)

  @overload(int, int)
  def __init__(self, X: int, Y: int) -> None:
    self.x = X
    self.y = Y

  @overload()
  def __init__(self) -> None:
    self.x = 0
    self.y = 0

  @overload(THIS)
  def __init__(self, other: Point) -> None:
    self.x = other.x
    self.y = other.y

  @overload(QPoint)
  def __init__(self, point: QPoint) -> None:
    self.x = point.x()
    self.y = point.y()

  @overload(QPointF)
  def __init__(self, point: QPointF) -> None:
    point = point.toPoint()
    self.x = point.x()
    self.y = point.y()

  @overload(QMouseEvent)
  def __init__(self, event: QMouseEvent) -> None:
    if TYPE_CHECKING:
      assert callable(self.__init__)
    point = event.pos()
    self.__init__(point)

  def __neg__(self) -> Self:
    """Returns the negation of this point."""
    return Point(-self.x, -self.y)

  def __add__(self, other: Self) -> Self:
    """Returns the sum of this point and another point."""
    cls = type(self)
    if isinstance(other, cls):
      return cls(self.x + other.x, self.y + other.y)
    return NotImplemented

  def __sub__(self, other: Self) -> Self:
    """Returns the difference of this point and another point."""
    return self + -other
