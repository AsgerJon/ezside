"""Line provides a class representation of a line in 2D space."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Callable

from worktoy.desc import AttriBox, Field
from worktoy.meta import BaseObject, overload

from ezside.tegning import Vector, Point
from moreworktoy import Config


class Line(BaseObject):
  """Line provides a class representation of a line in 2D space."""

  tolerance: float = Config('.tegning')['tolerance']

  p0 = AttriBox[Point]()
  r = AttriBox[Vector]()

  n = Field()
  e = Field()

  @n.GET
  def _getNormal(self) -> Vector:
    """Return the normal vector of the line."""
    return ~self.r

  @e.GET
  def _getEquation(self, ) -> Callable[[float], float]:
    """Return the equation of the line."""
    if self.r.x and self.r.y:
      n = self.n
      p0 = self.p0
      return lambda x: n.x * (x - p0.x) + n.y * (x - p0.y)
    if self.r.x:
      return lambda x: self.p0.y
    if self.r.y:
      e = """The line is vertical and has no equation!"""
      raise ValueError(e)
    e = """The direction vector for the line is the zero vector!"""
    raise ZeroDivisionError(e)

  def __contains__(self, point: Point) -> bool:
    """Return True if the point is on the line."""
    d = (self.e(point.x) - point.y) ** 2
    return True if d < self.tolerance else False

  @overload(Vector, Point)
  def __init__(self, direction: Vector, point: Point) -> None:
    """Initialize the line using a direction vector and a point."""
    self.r = direction
    self.p0 = point

  @overload(Point, Vector)
  def __init__(self, point: Point, direction: Vector) -> None:
    """Initialize the line using a point and a direction vector."""
    self.__init__(direction, point)

  @overload(Point, Point)
  def __init__(self, p0: Point, p1: Point) -> None:
    """Initialize the line using two points."""
    self.__init__(Vector(p0, p1), p0)

  @overload(int, int, int, int)
  def __init__(self, x0: int, y0: int, x1: int, y1: int) -> None:
    """Initialize the line using two points."""
    self.__init__(Point(x0, y0), Point(x1, y1))

  @overload(Point)
  def __init__(self, point: Point) -> None:
    """Initialize the line using a point."""
    self.__init__(Point(0, 0), point)

  @overload(Vector)
  def __init__(self, direction: Vector) -> None:
    """Initialize the line using a direction vector."""
    self.__init__(direction, Point(0, 0))
