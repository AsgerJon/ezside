"""AlignmentDescriptor implements the descriptor protocol for alignment
instances."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from attribox import AbstractDescriptor
from vistutils.waitaminute import typeMsg

from ezside.core import AlignCenter, parseAlignment, AlignFlag


class Alignment(AbstractDescriptor):
  """AlignmentDescriptor implements the descriptor protocol for alignment
  instances."""

  __default_alignment__ = None
  __fallback_alignment__ = AlignCenter

  def __init__(self, *args, **kwargs) -> None:
    alignment = parseAlignment(*args, **kwargs)
    if isinstance(alignment, AlignFlag):
      self.__default_alignment__ = alignment

  def __instance_get__(self, instance: object, owner: type, **kwargs) -> Any:
    """Implementation of the getter. The remaining functionality required
    by the descriptor protocol is implemented in the AbstractDescriptor
    class. """
    pvtName = self._getPrivateName()
    alignment = getattr(instance, pvtName, None)
    if alignment is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      setattr(instance, pvtName, self.__fallback_alignment__)
      return self.__instance_get__(instance, owner, _recursion=True)
    if isinstance(alignment, AlignFlag):
      return alignment
    e = typeMsg('alignment', alignment, AlignFlag, )
    raise TypeError(e)

  def __set__(self, instance: object, value: object, ) -> None:
    """Implementation of setter function."""
    pvtName = self._getPrivateName()
    if isinstance(value, AlignFlag):
      return setattr(instance, pvtName, value)
    if isinstance(value, tuple):
      return self.__set__(instance, [*value, ])
    if isinstance(value, list):
      args = []
      kwargs = {}
      for arg in value:
        if isinstance(arg, dict):
          kwargs = {**kwargs, **arg}
      return self.__set__(instance, parseAlignment(*args, **kwargs))
    if isinstance(value, (str, int)):
      return self.__set__(instance, [value, ])
    e = typeMsg('value', value, AlignFlag)
    raise TypeError(e)
