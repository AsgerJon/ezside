"""Point provides a dataclass representation of a point relative to some
coordinate system."""
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from typing import Self, TYPE_CHECKING, Any

from PySide6.QtCore import QPoint, QPointF
from PySide6.QtGui import QMouseEvent
from worktoy.desc import AttriBox, THIS, Field
from worktoy.base import BaseObject, overload
from worktoy.meta import DispatchException


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

  @overload(float, float)
  def __init__(self, X: float, Y: float) -> None:
    self.x = int(X)
    self.y = int(Y)

  @overload(complex)
  def __init__(self, Z: complex) -> None:
    self.x = int(Z.real)
    self.y = int(Z.imag)

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

  def _resolveOther(self, other: Any) -> Self:
    """Resolves the other argument to a point."""
    cls = type(self)
    if isinstance(other, cls):
      return other
    try:
      return cls(other)
    except DispatchException:
      return NotImplemented

  def __add__(self, other: Self) -> Self:
    """Returns the sum of this point and another point."""
    cls = type(self)
    other = self._resolveOther(other)
    if other is NotImplemented:
      return NotImplemented
    return cls(self.x + other.x, self.y + other.y)

  def __sub__(self, other: Self) -> Self:
    """Returns the difference of this point and another point."""
    return self + -other

  def __abs__(self, ) -> float:
    """Returns the absolute value of this point."""
    return (self.x ** 2 + self.y ** 2) ** 0.5

  def __mul__(self, other: Any) -> Self:
    """Returns the product of this point and a scalar."""
    cls = type(self)
    if isinstance(other, (int, float)):
      return cls(self.x * other, self.y * other)
    other = self._resolveOther(other)
    if other is NotImplemented:
      return NotImplemented
    return self.x * other.x + self.y * other.y

  def __truediv__(self, other: Any) -> Self:
    """Returns the quotient of this point and a scalar."""
    cls = type(self)
    if isinstance(other, (int, float)):
      if not other:
        raise ZeroDivisionError
      return cls(self.x / other, self.y / other)
    return NotImplemented
