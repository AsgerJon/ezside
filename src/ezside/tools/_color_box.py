"""ColorBox implements a color valued descriptor."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Never

from PySide6.QtGui import QColor, QBrush, QPen
from worktoy.desc import AbstractDescriptor
from worktoy.meta import overload
from worktoy.text import typeMsg


class ColorBox(AbstractDescriptor):
  __fallback_color__ = (255, 255, 255, 255,)
  __default_color__ = None

  @overload(QPen)
  def parse(self, pen: QPen) -> QColor:
    """Parses arguments to QColor instance"""
    return self.parse(pen.color(), )

  @overload(QBrush)
  def parse(self, brush: QBrush) -> QColor:
    """Parses arguments to QColor instance"""
    return self.parse(brush.color(), )

  @overload(QColor)
  def parse(self, color: QColor) -> QColor:
    """Parses arguments to QColor instance"""
    rgba = (color.red(), color.green(), color.blue(), color.alpha(),)
    return self.parse(*rgba, )

  @overload()
  def parse(self) -> QColor:
    """Parses arguments to QColor instance"""
    return self.parse(*self.__fallback_color__, )

  @overload(int)
  def parse(self, r: int) -> QColor:
    """Parses arguments to QColor instance"""
    return self.parse(r, r, r, 255)

  @overload(int, int, int)
  def parse(self, r: int, g: int, b: int) -> QColor:
    """Parses arguments to QColor instance"""
    return self.parse(r, g, b, 255)

  @overload(int, int, int, int)
  def parse(self, r: int, g: int, b: int, a: int) -> QColor:
    """Parses arguments to QColor instance"""
    return QColor(r, g, b, a)

  def __init__(self, *args) -> None:
    self.__default_color__ = self.parse(*args, )

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

  def __instance_set__(self, instance: object, value: Any) -> None:
    pvtName = self._getPrivateName()
    if isinstance(value, QColor):
      return setattr(instance, pvtName, value)
    color = self.parse(value)
    setattr(instance, pvtName, color)

  def __instance_del__(self, instance: object) -> Never:
    """Illegal deleter function"""
    e = """%s does not implement deletion!""" % self.__class__.__name__
    raise TypeError(e)
