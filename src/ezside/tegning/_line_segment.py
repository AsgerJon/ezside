"""Line represents a connection between two instances of Point. Please
note that the World instance is not aware of Line instances, but only of
Point instances. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from math import atan, pi
from typing import Never

from icecream import ic
from worktoy.desc import Field
from worktoy.meta import BaseObject, overload
from ezside.tegning import Point

ic.configureOutput(includeContext=True)


class LineSegment(BaseObject):
  """Line represents a connection between two instances of Point. Please
  note that the World instance is not aware of Line instances, but only of
  Point instances. """

  @classmethod
  def getTolerance(cls, ) -> float:
    """Return the epsilon value for the class."""
    return 1e-10

  __fallback_point__ = Point(0, 0)
  __start_point__ = None
  __end_point__ = None

  left = Field()
  top = Field()
  right = Field()
  bottom = Field()
  height = Field()
  width = Field()
  arg = Field()

  @overload()
  def __init__(self, ) -> None:
    pass

  @overload(Point, Point)
  def __init__(self, p1: Point, p2: Point) -> None:
    self.__start_point__ = p1
    self.__end_point__ = p2

  @overload(Point)
  def __init__(self, point: Point) -> None:
    self.__init__(self.__fallback_point__, point)

  @overload(int, int, int, int)
  def __init__(self, x1: int, y1: int, x2: int, y2: int) -> None:
    self.__init__(Point(x1, y1), Point(x2, y2))

  @overload(int, int)
  def __init__(self, x: int, y: int) -> None:
    self.__init__(Point(x, y))

  @left.GET
  def _getLeft(self) -> int:
    """Getter-function for the left."""
    return min(self.__start_point__.x, self.__end_point__.x)

  @top.GET
  def _getTop(self) -> int:
    """Getter-function for the top."""
    return min(self.__start_point__.y, self.__end_point__.y)

  @right.GET
  def _getRight(self) -> int:
    """Getter-function for the right."""
    return max(self.__start_point__.x, self.__end_point__.x)

  @bottom.GET
  def _getBottom(self) -> int:
    """Getter-function for the bottom."""
    return max(self.__start_point__.y, self.__end_point__.y)

  @height.GET
  def _getHeight(self) -> int:
    """Getter-function for the height."""
    return self.bottom - self.top

  @width.GET
  def _getWidth(self) -> int:
    """Getter-function for the width."""
    return self.right - self.left

  @arg.GET
  def _getArg(self) -> float:
    """Getter-function for the arg."""
    if self.height ** 2 + self.width ** 2:
      return atan(self.height / self.width)
    if self.width:
      return 0.
    if self.height:
      return pi / 2
    e = """The null line has no length and thus no argument!"""
    raise ZeroDivisionError(e)

  def __bool__(self, ) -> bool:
    """Returns True unless the line is the null line."""
    return True if self.height ** 2 + self.width ** 2 else False

  def __abs__(self, ) -> float:
    """Return the length of the line."""
    return (self.height ** 2 + self.width ** 2) ** 0.5

  @overload(Point)
  def __contains__(self, point: Point) -> bool:
    """Return whether the point is on the line."""
    return self.__contains__(point.x, point.y)

  @overload(int, int)
  def __contains__(self, x: int, y: int) -> bool:
    """Return whether the point is on the line."""
    if not self:
      return False
    if self.left > x or self.right < x:
      return False
    if self.top > y or self.bottom < y:
      return False
    return True if self._area(x, y) < self.getTolerance() else False

  def _area(self, x: float, y: float) -> float:
    """Return the area of the triangle formed by the line and the point."""
    left, top, right, bottom = self.left, self.top, self.right, self.bottom
    out = left * (bottom - y) + right * (y - top) - x * self.height
    return (out * out / 4) ** 0.5

  def __iter__(self, ) -> Never:
    """Not iterable."""
    e = """LineSegment is not iterable!"""
    raise TypeError(e)

  def __str__(self) -> str:
    """String representation"""
    P, Q = self.__start_point__, self.__end_point__
    return """LineSegment from %s to %s""" % (P, Q)

  def __repr__(self) -> str:
    """String representation"""
    P, Q = self.__start_point__, self.__end_point__
    return """LineSegment(%s, %s)""" % (P, Q)
