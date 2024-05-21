"""LayoutDescriptor provides a descriptor protocol for box layouts
allowing owners to defer the decision of orientation eliminating the need
for implementing the same widget twice to support both orientations. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QLayout
from attribox import AbstractDescriptor
from vistutils.waitaminute import typeMsg

from ezside.core import HORIZONTAL, VERTICAL, ORIENTATION


class LayoutDescriptor(AbstractDescriptor):
  """LayoutDescriptor provides a descriptor protocol for box layouts
  allowing owners to defer the decision of orientation eliminating the need
  for implementing the same widget twice to support both orientations. """

  __layout_classes__ = {
    HORIZONTAL: QHBoxLayout,
    VERTICAL  : QVBoxLayout
  }

  def __instance_get__(self, instance: object, owner: type, **kwargs) -> Any:
    """Explicit getter method"""
    pvtName = self._getPrivateName()
    layout = getattr(instance, pvtName, None)
    if layout is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      orientation = getattr(instance, 'orientation', None)
      if orientation is None:
        return self
      if not isinstance(orientation, ORIENTATION):
        e = typeMsg('orientation', orientation, ORIENTATION)
        raise TypeError(e)
      LayoutClass = self.__layout_classes__.get(orientation, )
      layout = LayoutClass()
      setattr(instance, pvtName, layout)
      return self.__instance_get__(instance, owner, _recursion=True)
    if isinstance(layout, QLayout):
      return layout
    e = typeMsg('layouts', layout, QLayout)
    raise TypeError(e)
