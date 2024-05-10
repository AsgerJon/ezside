"""ModInt provides a class of number like objects using modular arithmetic
to bound themselves within a range. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Callable


class ModMeta(type):
  """LMAO"""

  def wrapFactory(cls, callMeMaybe: Callable) -> Callable:
    """Factory wrapping the given functions"""
    # print('FACTORY: %s' % callMeMaybe.__name__)

    yolo = type('yolo', (), {
      '__inner_value__': 73,
      '__upper_bound__': 420,
      '__str__'        : lambda self: 'lmao!',
    })

    def wrapped(this, *args) -> ModInt:
      """Wraps the given function"""
      if not this.__upper_bound__:
        raise ZeroDivisionError
      if len(args) > 1:
        return callMeMaybe(this, *args)
      if not len(args):
        retValue = callMeMaybe(this.__inner_value__)
      else:
        that = [*args, None][0]
        retValue = callMeMaybe(this.__inner_value__, that)
      if isinstance(retValue, tuple):
        if all([isinstance(arg, int) for arg in retValue]):
          if 'div' in callMeMaybe.__name__:
            retValue = retValue[0]
      return cls(retValue, this.__upper_bound__)

    try:
      wrapped(yolo(), 420)
    except TypeError as typeError:
      if 'argument' in str(typeError):
        try:
          wrapped(yolo())
        except Exception as exception:
          raise exception from typeError

    return wrapped

  def __new__(mcls,
              name: str,
              bases: tuple,
              namespace: dict[str, Any]) -> ModMeta:
    """LMAO"""
    fakes = []
    stuff = [item for item in dir(int) if item not in namespace]
    baseCls = type.__new__(mcls, name, bases, namespace)
    for item in stuff:
      if item in ['__init__', '__init_subclass__', '__new__',
                  '__getattribute__', '__setattr__', '__delattr__',
                  '__getattr__', ]:
        continue
      if item in namespace:
        continue
      if getattr(int, item).__class__.__name__ == 'wrapper_descriptor':
        callMeMaybe = baseCls.wrapFactory(getattr(int, item))
        namespace |= {item: callMeMaybe}
    return type.__new__(mcls, name, (baseCls,), namespace)


class ModInt(metaclass=ModMeta):
  """ModInt provides a class of number like objects using modular arithmetic
  to bound themselves within a range. """

  __inner_value__ = None
  __upper_bound__ = None

  def __init__(self, val: int, lim: int, *args) -> None:
    self.__inner_value__ = val % (lim or 1)
    self.__upper_bound__ = lim

  def __str__(self, ) -> str:
    """String representation"""
    return 'N{%d}(%d)' % (self.__upper_bound__, self.__inner_value__)

  def __add__(self, other: Any) -> ModInt:
    """Addition"""
    if isinstance(other, int):
      return ModInt(self.__inner_value__ + other, self.__upper_bound__)
    if isinstance(other, ModInt):
      return self + other.__inner_value__
    if isinstance(other, float):
      if other.is_integer():
        return self + int(other)
    return NotImplemented

  def __repr__(self, ) -> str:
    """Representation"""
    return '%s(%d, %d)' % (self.__class__.__name__,
                           self.__inner_value__, self.__upper_bound__)
