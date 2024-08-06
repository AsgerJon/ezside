"""Fill encapsulates a QBrush for painting a solid fill."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import overload

from PySide6.QtGui import QColor
from worktoy.desc import AbstractDescriptor, Field
from worktoy.meta import overload
from worktoy.text import typeMsg


class Fill(AbstractDescriptor):
  """Fill encapsulates a QBrush for painting a solid fill."""

  def __instance_get__(self, instance: object, **kwargs) -> QColor:
    pvtName = self._getPrivateName()
    pvtColor = getattr(instance, pvtName, None)
    if pvtColor is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      setattr(instance, pvtName, self.__default_color__)
      return self.__instance_get__(instance, _recursion=True)
    if isinstance(pvtColor, QColor):
      return pvtColor
    e = typeMsg('pvtColor', pvtColor, QColor)
    raise TypeError(e)
