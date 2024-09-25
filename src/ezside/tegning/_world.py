"""World encapsulates a global coordinate system managing points. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Self, Never

from worktoy.meta import BaseObject, overload
from worktoy.parse import maybe

from ezside.tegning import Point


class World(BaseObject):
  """World provides a global coordinate system managing points. """

  __global_points__ = None
  __named_points__ = None
  __iter_contents__ = None

  def _getPoints(self, ) -> list[Point]:
    """Return the global points. """
    return maybe(self.__global_points__, [])

  def _getNamedPoints(self, ) -> dict[object, Point]:
    """Return the named points. """
    return maybe(self.__named_points__, {})

  @overload(Point)
  def addPoint(self, point: Point) -> Point:
    """Add a point to the global coordinate system. """
    pass

  @overload(int, int)
  def addPoint(self, x: int, y: int) -> Point:
    """Add a point to the global coordinate system. """
    pass

  def __contains__(self, point: Point) -> bool:
    """Return True if the point is in the global coordinate system. """
    for item in self:
      if item == point:
        return True
    return False

  def __iter__(self, ) -> Self:
    """Return an iterator over the global points. """
    self.__iter_contents__ = self._getPoints()
    return self

  def __next__(self, ) -> Point:
    """Return the next point in the global coordinate system. """
    try:
      return self.__iter_contents__.pop(0)
    except IndexError:
      raise StopIteration

  def __setitem__(self, key: object, value: Point) -> Never:
    clsName = self.__class__.__name__
    e = """The %s class does not support item assignment. """ % clsName
    raise TypeError(e)

  def __getitem__(self, key: object) -> Point:
    """Return the point with the given key. """
    for point in self:
      if point.label.lower() == str(key).lower():
        return point
    e = """No point with the label '%s' was found. """ % key
    raise KeyError(e)

  def __len__(self, ) -> int:
    """Return the number of points in the global coordinate system. """
    return len(self._getPoints())
