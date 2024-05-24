"""Orientation implements the descriptor protocol for instances of
Qt.Orientation."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from attribox import AbstractDescriptor
from vistutils.parse import maybe
from vistutils.waitaminute import typeMsg

from ezside.core import ORIENTATION, parseOrientation, HORIZONTAL


class Orientation(AbstractDescriptor):
  """The Orientation class implements the descriptor protocol for
  Qt.Orientation. """

  __default_orientation__ = None
  __fallback_orientation__ = HORIZONTAL

  def __init__(self, *args, **kwargs) -> None:
    orientation = parseOrientation(*args, **kwargs)
    if isinstance(orientation, ORIENTATION):
      self.__default_orientation__ = orientation

  def __instance_get__(self, instance: object, owner: type, **kwargs) -> Any:
    """Implementation of the getter. The remaining functionality required
    by the descriptor protocol is implemented in the AbstractDescriptor
    class. """
    pvtName = self._getPrivateName()
    orientation = getattr(instance, pvtName, None)
    if orientation is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      orientation = maybe(self.__default_orientation__,
                          self.__fallback_orientation__)
      setattr(instance, pvtName, orientation)
      return self.__instance_get__(instance, owner, _recursion=True)
    if isinstance(orientation, ORIENTATION):
      return orientation
    e = typeMsg('orientation', orientation, ORIENTATION, )
    raise TypeError(e)

  def __set__(self, instance: object, value: object, ) -> None:
    """Implementation of setter function."""
    pvtName = self._getPrivateName()
    orientation = parseOrientation(value)
    if isinstance(orientation, ORIENTATION):
      setattr(instance, pvtName, orientation)
    else:
      e = typeMsg('orientation', orientation, ORIENTATION)
      raise TypeError(e)
