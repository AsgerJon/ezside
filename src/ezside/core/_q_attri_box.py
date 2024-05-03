"""QAttriBox inherits from AttriBox such that accessor functions emit
signals. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Optional, Any, Never

from PySide6.QtCore import QObject, Signal
from attribox import AttriBox
from vistutils.waitaminute import typeMsg


class _QObjectDescriptor:
  """_QObjectDescriptor is a descriptor that emits signals when accessed."""

  __field_name__ = None
  __field_owner__ = None
  __signal_types__ = None

  def __init__(self, *args, ) -> None:
    for arg in args:
      if not isinstance(arg, type):
        e = typeMsg('arg', arg, type)
        raise TypeError(e)
    self.__signal_types__ = [*args]

  def __set_name__(self, owner: type, name: str) -> None:
    """Sets the name and owner of the instance"""
    if self.__field_name__ is not None or self.__field_owner__ is not None:
      raise AttributeError("Cannot set name and owner twice.")
    self.__field_name__ = name
    self.__field_owner__ = owner

  def _getPrivateName(self, ) -> str:
    """Getter-function for private name"""
    return '_%s' % self.__field_name__

  def _createInnerObject(self, instance: object) -> None:
    """Create the inner object."""

  def __get__(self, instance: object, owner: type, **kwargs) -> Any:
    """Emits a signal when accessed."""
    if instance is None:
      return self
    pvtName = self._getPrivateName()
    innerObject = getattr(instance, pvtName, None)
    if innerObject is None:
      try:
        setattr(owner, pvtName, Signal(*self.__signal_types__))
      except AttributeError as attributeError:
        e = """Only classes allowing dynamic attributes can use QAttriBox."""
        raise TypeError(e) from attributeError

  def __set__(self, *_) -> Never:
    """Illegal setter function"""
    e = """_QObjectDescriptor is read-only."""
    raise TypeError(e)

  def __del__(self, *_) -> Never:
    """Illegal deleter function"""
    e = """_QObjectDescriptor cannot be deleted."""
    raise TypeError(e)


class WrappedQObject:
  """LMAO"""

  __inner_object__ = None

  def __init__(self, *args, **kwargs) -> None:
    self.__inner_object__ = QObject(*args, **kwargs)


class QAttriBox(QObject, AttriBox):
  """QAttriBox inherits from AttriBox such that accessor functions emit
  signals. """
 