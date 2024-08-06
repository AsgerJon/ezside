"""MarginsBox provides QMarginsF valued descriptor class."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtCore import QMarginsF, QMargins
from worktoy.desc import AbstractDescriptor
from worktoy.meta import overload
from worktoy.text import typeMsg, monoSpace


class MarginsBox(AbstractDescriptor):
  """MarginsBox provides QMarginsF valued descriptor class."""

  __fallback_margins__ = (1, 1, 1, 1,)
  __default_margins__ = None

  def _getFallbackMargins(self, ) -> QMarginsF:
    """Get the fallback margins."""
    return QMarginsF(*self.__fallback_margins__, )

  @overload(QMargins)
  @overload(QMarginsF)
  def parse(self, margins: QMarginsF) -> QMarginsF:
    """Parses arguments to QMarginsF instance"""
    return self.parse(margins.left(),
                      margins.top(),
                      margins.right(),
                      margins.bottom(), )

  @overload(int, int)
  @overload(float, float)
  def parse(self, width: float, height: float) -> QMarginsF:
    """Parses arguments to QMarginsF instance"""
    return self.parse(width, height, width, height, )

  @overload(int)
  @overload(float)
  def parse(self, value: float) -> QMarginsF:
    """Parses arguments to QMarginsF instance"""
    return self.parse(value, value, value, value, )

  @overload()
  def parse(self) -> QMarginsF:
    """Parses arguments to QMarginsF instance"""
    return self.parse(*self.__fallback_margins__, )

  @overload(int, int, int, int)
  @overload(float, float, float, float)
  def parse(self, *args) -> QMarginsF:
    """Parses arguments to QMarginsF instance"""
    left, top, right, bottom = None, None, None, None
    for arg in args:
      if left is None:
        left = float(arg)
      elif top is None:
        top = float(arg)
      elif right is None:
        right = float(arg)
      elif bottom is None:
        bottom = float(arg)
        break
    else:
      e = """Unable to parse arguments!"""
      raise ValueError(e)
    return QMarginsF(left, top, right, bottom, )

  def __init__(self, *args) -> None:
    """The constructor method for the MarginsBox descriptor."""
    AbstractDescriptor.__init__(self)
    self.__default_margins__ = self.parse(*args, )

  def _getPrivateName(self) -> str:
    """Get the private name of the descriptor."""
    return '__%s_value__' % self.getFieldName()

  def __instance_get__(self, instance: object, **kwargs) -> QMarginsF:
    """Get the value of the field."""
    pvtName = self._getPrivateName()
    pvtValue = getattr(instance, pvtName, None)
    if pvtValue is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      setattr(instance, pvtName, self.__default_margins__)
      return self.__instance_get__(instance, _recursion=True)
    if isinstance(pvtValue, QMarginsF):
      return pvtValue
    e = typeMsg(pvtName, pvtValue, QMarginsF)
    raise TypeError(monoSpace(e))

  def __instance_set__(self, instance: object, value: QMarginsF) -> None:
    """Set the value of the field."""
    margins = self.parse(value)
    pvtName = self._getPrivateName()
    setattr(instance, pvtName, value)
