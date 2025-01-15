"""Vector2D encapsulates a 2D vector. It includes common vector
operations, such as addition, subtraction, and scalar multiplication on an
element wise basis. Additionally, it implements the dot product and the
determinant of two vectors mapped to the __mul__ and __matmul__ operators
respectively."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self

from PySide6.QtCore import QPointF, QPoint
from PySide6.QtGui import QVector2D, QEventPoint
from worktoy.text import monoSpace
from worktoy.desc import AttriBox, THIS, Field
from worktoy.base import BaseObject, overload

from . import Point

try:
  from moreworktoy.config import Eps
except ImportError:
  Eps = lambda *args: [*args, 1e-6][0]

try:
  from moreworktoy.math import atan2
except ImportError:
  from math import atan2


class Vector2D(BaseObject):
  """Vector2D encapsulates a 2D vector. It includes common vector
  operations, such as addition, subtraction, and scalar multiplication on an
  element wise basis. Additionally, it implements the dot product and the
  determinant of two vectors mapped to the __mul__ and __matmul__ operators
  respectively."""

  eps = Eps(1e-06)

  x = AttriBox[float](0.0)
  y = AttriBox[float](0.0)

  Q = Field()

  @overload(float, float)
  def __init__(self, x: float, y: float) -> None:
    """Vector2D is initialized with two floats. """
    self.x = x
    self.y = y

  @overload(int, int)
  def __init__(self, x: int, y: int) -> None:
    """Vector2D is initialized with two integers. """
    self.x = float(x)
    self.y = float(y)

  @overload(complex)
  def __init__(self, z: complex) -> None:
    """Vector2D is initialized with a complex number. """
    self.x = z.real
    self.y = z.imag

  @overload(QPointF)
  def __init__(self, p: QPointF) -> None:
    """Vector2D is initialized with a QPointF. """
    self.x = p.x()
    self.y = p.y()

  @overload(QPoint)
  def __init__(self, p: QPoint) -> None:
    """Vector2D is initialized with a QPoint. """
    self.x = float(p.x())
    self.y = float(p.y())

  @overload(QPointF, QPointF)
  def __init__(self, p1: QPointF, p2: QPointF) -> None:
    """Vector2D is initialized with two QPointF. """
    self.x = p2.x() - p1.x()
    self.y = p2.y() - p1.y()

  @overload(QPoint, QPoint)
  def __init__(self, p1: QPoint, p2: QPoint) -> None:
    """Vector2D is initialized with two QPoint. """
    self.x = float(p2.x() - p1.x())
    self.y = float(p2.y() - p1.y())

  @overload(QVector2D)
  def __init__(self, v: QVector2D) -> None:
    """Vector2D is initialized with a QVector2D. """
    self.x = v.x()
    self.y = v.y()

  @overload(THIS)
  def __init__(self, v: THIS) -> None:
    """Vector2D is initialized with another Vector2D. """
    if TYPE_CHECKING:
      cls = type(self)
      assert isinstance(v, cls)
    self.x = v.x
    self.y = v.y

  @overload(Point, Point)
  def __init__(self, p1: Point, p2: Point) -> None:
    """Vector2D is initialized with two Points. """
    self.x = p2.x - p1.x
    self.y = p2.y - p1.y

  @overload(Point)
  def __init__(self, p: Point) -> None:
    """Vector2D is initialized with a Point. """
    self.x = p.x
    self.y = p.y

  @overload(QEventPoint)
  def __init__(self, p: QEventPoint) -> None:
    """Vector2D is initialized with a QEventPoint. """
    if TYPE_CHECKING:
      assert callable(self.__init__)
    p1 = QEventPoint.lastPos(p)
    p2 = QEventPoint.pos(p)
    self.__init__(p1, p2)

  @overload()
  def __init__(self) -> None:
    """Vector2D is initialized with default values. """
    self.x = 0.0
    self.y = 0.0

  @Q.GET
  def _getQVersion(self) -> QVector2D:
    """Returns the Qt version of this vector."""
    return QVector2D(self.x, self.y)

  def __abs__(self, ) -> float:
    """Returns the length of the vector. """
    return (self.x ** 2 + self.y ** 2) ** 0.5

  def __bool__(self) -> bool:
    """Returns True if the vector is non-zero. """
    return True if self * self < self.eps else False

  def __add__(self, other: Any) -> Self:
    """Returns the sum of this vector and another. """
    cls = type(self)
    other = cls(other)
    return cls(self.x + other.x, self.y + other.y)

  def __sub__(self, other: Any) -> Self:
    """Returns the difference of this vector and another. """
    cls = type(self)
    other = cls(other)
    return cls(self.x - other.x, self.y - other.y)

  def __neg__(self, ) -> Self:
    """Returns the negation of this vector. """
    cls = type(self)
    return cls(-self.x, -self.y)

  def __pos__(self) -> Self:
    """Returns this vector. """
    cls = type(self)
    return cls(abs(self.x), abs(self.y))

  def __mul__(self, other: Any) -> Any:
    """Returns the dot product of this vector and another. """
    cls = type(self)
    if TYPE_CHECKING:
      assert isinstance(self.x, float)
      assert isinstance(self.y, float)
    if isinstance(other, (float, int)):  # Scalars
      return cls(float(self.x * other), float(self.y * other))
    other = cls(other)
    return self.x * other.x + self.y * other.y

  def __truediv__(self, other: Any) -> Any:
    """Returns the element wise division of this vector and a scalar. """
    cls = type(self)
    if not self:
      return self
    if not other:
      e = """%s received zero divisor!""" % cls.__name__
      raise ZeroDivisionError(monoSpace(e))
    if isinstance(other, (float, int)):
      return self * (1 / other)
    other = cls(other)
    if other.x and other.y:
      return cls(self.x / other.x, self.y / other.y)
    if other.x:  # other.y == 0, ok if self.y == 0
      if self.y:
        e = """%s received zero divisor!""" % cls.__name__
        raise ZeroDivisionError(monoSpace(e))
      return self.x / other.x
    if other.y:  # other.x == 0, ok if self.x == 0
      if self.x:
        e = """%s received zero divisor!""" % cls.__name__
        raise ZeroDivisionError(monoSpace(e))
      return self.y / other.y

  def __matmul__(self, other: Any) -> float:
    """Returns the determinant of this vector and another. """
    cls = type(self)
    other = cls(other)
    return self.x * other.y - self.y * other.x

  def __len__(self, ) -> float:
    """Returns the dimensionality of the vector. """
    return 2

  def __iadd__(self, other: Any) -> Self:
    """Adds another vector to this one. """
    cls = type(self)
    if isinstance(other, (float, int)):
      self.x += other
      self.y += other
      return self
    other = cls(other)
    self.x += other.x
    self.y += other.y
    return self

  def __isub__(self, other: Any) -> Self:
    """Subtracts another vector from this one. """
    cls = type(self)
    if isinstance(other, (float, int)):
      self.x -= other
      self.y -= other
      return self
    other = cls(other)
    self.x -= other.x
    self.y -= other.y
    return self

  def __imul__(self, other: Any) -> Self:
    """Multiplies this vector by a scalar. """
    cls = type(self)
    if isinstance(other, (float, int)):
      self.x *= other
      self.y *= other
      return self
    return NotImplemented

  def __itruediv__(self, other: Any) -> Self:
    """Divides this vector by a scalar. """
    cls = type(self)
    if isinstance(other, (float, int)):
      if other:
        self.x /= other
        self.y /= other
        return self
      e = """%s received zero divisor!""" % cls.__name__
      raise ZeroDivisionError(monoSpace(e))
    return NotImplemented

  def __imatmul__(self, other: Any) -> Self:
    """Calculates the determinant of this vector and another. """
    return self.__imul__(other)

  def __radd__(self, other: Any) -> Self:
    """Adds this vector to another. """
    return self.__add__(other)

  def __rsub__(self, other: Any) -> Self:
    """Subtracts this vector from another. """
    return self.__neg__().__add__(other)

  def __rmul__(self, other: Any) -> Any:
    """Multiplies this vector by a scalar. """
    return self.__mul__(other)

  def __rtruediv__(self, other: Any) -> Any:
    """Divides this vector by a scalar. """
    if self:
      return self.__truediv__(other)
    e = """%s received zero divisor!""" % type(self).__name__
    raise ZeroDivisionError(monoSpace(e))

  def __rmatmul__(self, other: Any) -> float:
    """Calculates the determinant of this vector and another. """
    if self:
      return self.__matmul__(other)
    e = """%s received zero divisor!""" % type(self).__name__
    raise ZeroDivisionError(monoSpace(e))

  def __mod__(self, other: Any) -> Self:
    """Returns the element wise modulus of this vector and another. """
    cls = type(self)
    if isinstance(other, (float, int)):
      return cls(self.x % other, self.y % other)
    other = cls(other)
    return cls(self.x % other.x, self.y % other.y)

  def __imod__(self, other: Any) -> Self:
    """Calculates the element wise modulus of this vector and another. """
    cls = type(self)
    if isinstance(other, (float, int)):
      self.x %= other
      self.y %= other
      return self
    other = cls(other)
    self.x %= other.x
    self.y %= other.y
    return self

  def __rmod__(self, other: Any) -> Self:
    """Calculates the element wise modulus of this vector and another. """
    return self.__mod__(other)

  def unit(self) -> Self:
    """Returns the unit vector of this vector. """
    cls = type(self)
    if not self:
      return self
    return self / abs(self)

  def angle(self) -> float:
    """Returns the angle of the vector. """
    if self:
      return atan2(self.y, self.x)
    e = """The zero vector has no angle!"""
    raise ValueError(monoSpace(e))
