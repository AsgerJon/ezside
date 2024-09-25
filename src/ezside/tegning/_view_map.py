"""ViewMap transforms points from global to local coordinates. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox
from worktoy.meta import BaseObject, overload

from ezside.tegning import Point


class ViewMap(BaseObject):
  """ViewMap transforms points from global to local coordinates. """

  P0 = AttriBox[Point]()
  s = AttriBox[float](0.0)
  t = AttriBox[float](0.0)

  @overload(int, int, float, float)
  def __init__(self, x0: int, y0: int, s: float, t: float) -> None:
    """Initialize the view map. """
    self.__init__(Point(x0, y0), s, t)

  @overload(Point, float, float)
  def __init__(self, p0: Point, s: float, t: float) -> None:
    """Initialize the view map. """
    self.P0 = p0
    self.s = s
    self.t = t

  @overload(int, int, float)
  def __init__(self, x0: int, y0: int, s: float) -> None:
    self.__init__(Point(x0, y0), s, s)

  @overload(Point, float)
  def __init__(self, p0: Point, s: float) -> None:
    self.__init__(p0, s, s)

  @overload(int, int)
  def __init__(self, x0: int, y0: int) -> None:
    self.__init__(Point(x0, y0), .0, .0)

  @overload(Point)
  def __init__(self, p0: Point) -> None:
    self.__init__(p0, .0, .0)

  @overload()
  def __init__(self) -> None:
    self.__init__(Point(), .0, .0)

  def __call__(self, point: Point) -> Point:
    """Return the point transformed to local coordinates. """
