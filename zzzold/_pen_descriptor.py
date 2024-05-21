"""Descriptor protocol implementation for instances requiring attributes
of QPen type."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtGui import QPen
from attribox import AbstractDescriptor
from vistutils.waitaminute import typeMsg

from ezside.core import parsePen


class PenDescriptor(AbstractDescriptor):
  """Descriptor protocol implementation for instances requiring attributes
  of QPen type."""

  __pos_args__ = None
  __pos_kwargs__ = None

  def __init__(self, *args, **kwargs) -> None:
    """Initialize the descriptor."""
    self.__pos_args__ = args
    self.__pos_kwargs__ = kwargs

  def _createInstance(self, ) -> QPen:
    """Create the QPen instance."""
    return parsePen(self.__pos_args__)

  def __instance_get__(self, instance: object, owner: type, **kwargs) -> Any:
    """Explicit getter-function for the QPen instance."""
    if instance is None:
      return self
    pvtName = self._getPrivateName()
    if getattr(instance, pvtName, None) is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      pen = self._createInstance()
      setattr(instance, pvtName, pen)
      return self.__instance_get__(instance, owner, _recursion=True)
    pen = getattr(instance, pvtName)
    if isinstance(pen, QPen):
      return pen
    e = typeMsg(pen, QPen)
    raise TypeError(e)
