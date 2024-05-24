"""Wait provides a simplified version of the AttriBox."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Callable, Self, Any

from attribox import scope, this
from vistutils.parse import maybe
from vistutils.waitaminute import typeMsg


class Wait:
  """Wait provides a simplified version of the AttriBox."""

  __pos_args__ = None
  __key_args__ = None
  __field_name__ = None
  __field_owner__ = None
  __callback_function__ = None

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the Wait object."""
    self.__pos_args__ = args
    self.__key_args__ = kwargs

  def __set_name__(self, owner: type, name: str) -> None:
    """Sets the name of the field."""
    self.__field_name__ = name
    self.__field_owner__ = owner

  def _setCallback(self, callMeMaybe: Callable) -> Callable:
    """Sets the callback function."""
    if self.__callback_function__ is not None:
      e = """The callback function has already been set. """
      raise AttributeError(e)
    if callable(callMeMaybe):
      self.__callback_function__ = callMeMaybe
      return callMeMaybe
    e = typeMsg('callMeMaybe', callMeMaybe, Callable)
    raise TypeError(e)

  def _getCallback(self, *args, **kwargs) -> Callable:
    """Gets the callback function."""
    return maybe(self.__callback_function__, lambda *a, **k: (a, k))

  def __matmul__(self, callMeMaybe: Callable) -> Self:
    """Sets the callback function."""
    self._setCallback(callMeMaybe)
    return self

  def __rmatmul__(self, callMeMaybe: Callable) -> Self:
    """Sets the callback function."""
    return self @ callMeMaybe

  def _getPosArgs(self, instance: object, ) -> list:
    """Returns the positional arguments."""
    out = []
    for arg in self.__pos_args__:
      if arg is this:
        out.append(instance, )
      elif arg is scope:
        out.append(self.__field_owner__, )
      else:
        out.append(arg, )
    return out

  def _getKeyArgs(self, instance: object) -> dict:
    """Returns the keyword arguments."""
    out = {}
    for (key, arg) in self.__key_args__.items():
      if arg is this:
        out[key] = instance
      elif arg is scope:
        out[key] = self.__field_owner__
      else:
        out[key] = arg
    return out

  def __get__(self, instance: object, owner: type, **kwargs) -> Any:
    """Returns the Wait object."""
    if instance is None:
      return self
    callMeMaybe = self._getCallback()
    args = self._getPosArgs(instance)
    kwargs = self._getKeyArgs(instance)
    return callMeMaybe(*args, **kwargs)
