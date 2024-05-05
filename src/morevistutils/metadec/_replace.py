"""The strName function provides the basic functionality for the metadec
module. It changes the __str__ method to return the '__qualname__'
attribute of the object. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from types import MethodType, FunctionType
from typing import Callable

from vistutils.text import monoSpace
from vistutils.waitaminute import typeMsg


class Replace:
  """The strName function provides the basic functionality for the metadec
  module. It changes the __str__ method to return the '__qualname__'
  attribute of the object. """

  __attribute_name__ = None
  __replacement_method__ = None

  def _setAttributeName(self, attributeName: str) -> None:
    """Set the attribute name of the StrName object."""
    self.__attribute_name__ = attributeName

  def _getAttributeName(self) -> str:
    """Getter-function for the attribute name."""
    return self.__attribute_name__

  def _setReplacementMethod(self, callMeMaybe: Callable) -> None:
    """Set the replacement method of the StrName object."""
    if callable(callMeMaybe):
      self.__replacement_method__ = callMeMaybe
    else:
      e = typeMsg('callMeMaybe', callMeMaybe, Callable)
      raise TypeError(e)

  def _getReplacementMethod(self, ) -> Callable:
    """Getter-function for the replacement method."""
    return self.__replacement_method__

  def _apply(self, obj: type | FunctionType) -> object:
    """Apply the StrName object to the class."""
    name = self._getAttributeName()
    replacement = MethodType(self._getReplacementMethod(), obj)
    if isinstance(obj, type) or isinstance(obj, FunctionType):
      setattr(obj, name, replacement)
      return obj
    e = typeMsg('obj', obj, type)
    raise TypeError(e)

  def __call__(self, obj: type | FunctionType) -> object:
    """Apply the StrName object to the class."""
    return self._apply(obj)
