"""YOLO"""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Callable

from vistutils.waitaminute import typeMsg


class Sussinator:
  """LMAO"""

  __target_type__ = None

  def __init__(self, targetType: type) -> None:
    """LMAO"""
    if not isinstance(targetType, type):
      e = typeMsg('targetType', targetType, type)
      raise TypeError(e)
    self.__target_type__ = targetType

  def __call__(self, realClass: type) -> type:
    """LMAO"""
    if not isinstance(realClass, type):
      e = typeMsg('realClass', realClass, type)
      raise TypeError(e)
    metaClass = type(realClass)
    name = realClass.__name__
    bases = (realClass, self.__target_type__,)
    namespace = dict(__is_sus__=True, )
    return metaClass(name, bases, namespace, )
