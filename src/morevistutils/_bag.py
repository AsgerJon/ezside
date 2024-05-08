"""Bag provides a clojure-like way of setting instantiation arguments
ahead of time."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Self, Any, Callable

from icecream import ic
from vistutils.fields import EmptyField
from vistutils.waitaminute import typeMsg

ic.configureOutput(includeContext=True, )


class Bag:
  """Bag provides allows setting instantiation arguments ahead of time. """
  __iter_contents__ = None

  __field_owner__ = None
  __field_name__ = None
  __field_class__ = None

  __pos_args__ = None
  __key_args__ = None
  __inner_class__ = None

  cls = EmptyField()
  posArgs = EmptyField()
  keyArgs = EmptyField()
  inner = EmptyField()

  @cls.GET
  def _getCls(self) -> type:
    """Getter-function for inner class"""
    return self.__inner_class__

  @posArgs.GET
  def _getPosArgs(self) -> list:
    """Getter-function for positional arguments"""
    return [*self.__pos_args__, ]

  @keyArgs.GET
  def _getKeyArgs(self) -> dict:
    """Getter-function for keyword arguments"""
    return {**self.__key_args__, }

  def __init__(self, *args, **kwargs) -> None:
    """Initialize the bag with arguments"""
    self.__pos_args__ = args
    self.__key_args__ = kwargs

  def __set_name__(self, owner: type, name: str) -> None:
    """This does actually trigger when on the right hand side of @ in a
    class body!"""
    self.__field_owner__ = owner
    self.__field_name__ = name

  def __matmul__(self, other: type) -> Self:
    """Sets other as __later_cls__"""
    if not isinstance(other, type):
      return NotImplemented
    if self.__inner_class__ is not None:
      e = """Cannot set __later_cls__ twice. """
      raise AttributeError(e)

    baseNew = getattr(other, '__new__', )
    if not callable(baseNew):
      e = typeMsg('new', baseNew, Callable)
      raise TypeError(e)

    def newPlus(scope: type, *args, **kwargs) -> Any:
      """Create a new instance of the inner class"""
      this = baseNew(scope, *args, **kwargs)
      self.registerInstance(this, )
      return this

    setattr(other, '__new__', newPlus, )

    self.__inner_class__ = other

    return self

  def _getPrivateFieldName(self) -> str:
    """Returns the name of the private attribute used to store the inner
    object. """
    return '_%s' % self.__field_name__

  def registerInstance(self, instance: object, ) -> None:
    """Register the instance"""
    if self.__field_owner__ is None:
      e = """The field owner has not been set. """
      raise AttributeError(e)
    if self.__field_name__ is None:
      e = """The field name has not been set. """
      raise AttributeError(e)
    pvtName = self._getPrivateFieldName()
    setattr(self, pvtName, instance)

  def __call__(self, *args, **kwargs) -> Self:
    """Returns the class and arguments"""
    self.__pos_args__ = [*self.__pos_args__, *args]
    self.__key_args__ = {**self.__key_args__, **kwargs}
    return self

  def __rmatmul__(self, other: type) -> Self:
    """Sets other as __later_cls__"""
    return self @ other

  def __iter__(self, ) -> Self:
    """Iterate through the bag"""
    self.__iter_contents__ = [self.cls, self.posArgs, self.keyArgs]
    return self

  def __next__(self, ) -> Any:
    """Iterate through the bag"""
    try:
      return self.__iter_contents__.pop(0)
    except IndexError:
      raise StopIteration

  @inner.GET
  def _getInnerObject(self) -> Any:
    """Returns the inner object. """
    pvtName = self._getPrivateFieldName()
    if not hasattr(self, pvtName):
      e = """The inner object has not been assigned. """
      raise AttributeError(e)
    return getattr(self, pvtName)
