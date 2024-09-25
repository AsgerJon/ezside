"""Point provides a data class for points in the World class. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox
from worktoy.ezdata import EZData
from worktoy.meta import BaseObject, overload
from worktoy.parse import maybe


class Point(BaseObject):
  """  A class to represent a point within a precise coordinate system
  tailored for various scales of measurement, suitable for
  applications like floor plans, GIS, and machine part mapping.
  The class uses integer coordinates and a scale factor to manage
  the representation's precision, adapting to different requirements
  such as meters, kilometers, or millimeters.

  Attributes:
    x (int): The x-coordinate of the point, expressed in integer
             units. This integer represents a step within the
             coordinate system along the horizontal axis, which
             will be scaled to represent real-world distances.
    y (int): The y-coordinate of the point, expressed in integer
             units. This integer represents a step within the
             coordinate system along the vertical axis, which
             will be scaled to represent real-world distances.
    label (str): The label of the point, expressed as a string. Must be
    unique. One will be auto generated if necessary."""

  __registered_names__ = None

  @classmethod
  def _getNames(cls) -> list[str]:
    """Getter-function for list of registered names"""
    return maybe(cls.__registered_names__, [])

  @classmethod
  def _registerName(cls, name: str, **kwargs) -> str:
    """Registers the given name. By default, if name is not unique,
    a unique one is generated. Change this behavior by setting the
    'strict' keyword argument to True. The method returns the unique name."""
    names = cls._getNames()
    if name in names:
      if kwargs.get('strict', False):
        e = """Name '%s' is already registered!""" % name
        raise ValueError(e)
      if kwargs.get('_recursion', False):
        raise RecursionError
      newName = cls._generateUniqueName(name)
      return cls._registerName(newName, _recursion=True)
    cls.__registered_names__ = [*names, name]
    return name

  @staticmethod
  def _generateUniqueName(name: str) -> str:
    """Generates a unique name based on the given name."""
    if name.split('_')[-1].isdigit():
      old = name.split('_')[-1]
      base = name[:-(len(old) + 1)]
      while old:
        if old[0] != '0':
          old = int(old) + 1
          break
        old = old[1:]
      else:
        old = 0
      return """%s_%03d""" % (base, old)
    return name + '_%03d' % 0

  x = AttriBox[int]()
  y = AttriBox[int]()
  label = AttriBox[str]()

  @overload(int, int, str)
  def __init__(self, x: int, y: int, label_: str) -> None:
    self.x = x
    self.y = y
    self.label = label_

  @overload(int, int)
  def __init__(self, x: int, y: int) -> None:
    self.__init__(x, y, self.__str__())

  @overload()
  def __init__(self) -> None:
    self.__init__(0, 0)

  @overload(int, int)
  def __eq__(self, x: int, y: int) -> bool:
    return False if (self.x - x) * (self.y - y) else True

  def __str__(self) -> str:
    """String representation"""
    return """Point(%d, %d)""" % (self.x, self.y)

  def __repr__(self) -> str:
    """String representation"""
    return """Point(%d, %d)""" % (self.x, self.y)
