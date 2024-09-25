"""Vector provides a class representation of a vector in 2D space."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any
from cmath import phase

from worktoy.desc import AttriBox
from worktoy.meta import BaseObject, overload

from ezside.tegning import Point


class Vector(BaseObject):
  """Vector provides a class representation of a vector in 2D space."""

  x = AttriBox[float]()
  y = AttriBox[float]()

  @overload(float, float)
  def __init__(self, x: float, y: float) -> None:
    """Initialize the vector. """
    self.x = x
    self.y = y

  @overload()
  def __init__(self) -> None:
    """Initialize the vector. """
    self.__init__(.0, .0)

  @overload(Point, Point)
  def __init__(self, p0: Point, p1: Point) -> None:
    """Initialize the vector. """
    self.__init__(p1.x - p0.x, p1.y - p0.y)

  @overload(Point)
  def __init__(self, point: Point) -> None:
    """Initialize the vector. """
    self.__init__(point.x, point.y)

  def __mul__(self, other: object) -> Any:
    """Return the vector multiplied by a scalar. """
    if isinstance(other, (int, float)):
      return Vector(self.x * other, self.y * other)
    if isinstance(other, type(self)):
      return self.x * other.x + self.y * other.y
    return NotImplemented

  def __rmul__(self, other: object) -> Any:
    """Return the vector multiplied by a scalar. """
    if isinstance(other, (int, float)):
      return Vector(self.x * other, self.y * other)
    return NotImplemented

  def __abs__(self) -> float:
    """Return the magnitude of the vector. """
    return (self.x ** 2 + self.y ** 2) ** .5

  def __complex__(self) -> complex:
    """Return the vector as a complex number. """
    return self.x + self.y * 1j

  def arg(self) -> float:
    """Return the angle of the vector. """
    return phase(self.__complex__())

  def __add__(self, other: object) -> Any:
    """Return the vector added to another vector. """
    if isinstance(other, type(self)):
      return Vector(self.x + other.x, self.y + other.y)
    return NotImplemented

  def __neg__(self) -> Vector:
    """Return the negated vector. """
    return Vector(-self.x, -self.y)

  def __sub__(self, other: object) -> Any:
    """Return the vector subtracted by another vector. """
    if isinstance(other, type(self)):
      return self + -other
    return NotImplemented

  def __invert__(self) -> Vector:
    """Return the vector rotated 90 degrees. """
    return Vector(-self.y, self.x)

  def __truediv__(self, other: object) -> Any:
    """Return the vector divided by a scalar. """
    if isinstance(other, (int, float)):
      return Vector(self.x / other, self.y / other)
    return NotImplemented

  def __rshift__(self, other: object) -> Any:
    """If other is a vector, this operation returns a new vector that is
    this vector projected onto the other vector. """
    if isinstance(other, type(self)):
      return other * (self * other) / abs(other) ** 2
    return NotImplemented

  def __rlshift__(self, other: object) -> Any:
    """If other is a vector, this operation returns a new vector that is
    the other vector projected onto this vector. """
    if isinstance(other, type(self)):
      return self >> other
    return NotImplemented
