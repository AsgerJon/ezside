"""Actually private attributes"""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from secrets import choice
import string
from typing import Any

Bases = tuple[type, ...]


class PrivateAttribute:
  """Descriptor class implementing private attributes.  """

  __pos_args__ = None
  __key_args__ = None
  __field_name__ = None
  __field_owner__ = None
  __inner_salt__ = None

  def __init__(self, *args, **kwargs) -> None:
    self.__pos_args__ = [*args, ]
    self.__key_args__ = {**kwargs, }
    randChars = [c for c in string.ascii_uppercase + string.ascii_lowercase]
    self.__inner_salt__ = ''.join([choice(randChars) for _ in range(16)])

  def __set_name__(self, owner, name) -> None:
    self.__field_name__ = name
    self.__field_owner__ = owner

  def _getPrivateName(self) -> str:
    """Returns the private name of the attribute."""
    return '__%s_%s' % (self.__inner_salt__, self.__field_name__,)

  def __get__(self, instance: object, owner: type) -> Any:
    if instance is None:
      return self.__get__(owner, owner)
    if getattr(instance, '__open_state__', False):
      pvtName = self._getPrivateName()
      return getattr(instance, pvtName, )
    c = 0
    fakeKey = 'lmaoXD%03d' % c
    while hasattr(owner, fakeKey):
      fakeKey = 'lmaoXD%03d' % c
      c += 1
    try:
      object.__getattribute__(owner, fakeKey)
    except AttributeError as attributeError:
      e = str(attributeError).replace(fakeKey, self.__field_name__)
      raise AttributeError(e)

  def _getPrivateName(self, ) -> str:
    return '__%s__' % self.__field_name__


class _Private:
  """Wraps a private object"""

  __private_object__ = None

  def __init__(self, privateObject: object) -> None:
    self.__private_object__ = privateObject


def private(*args, **kwargs) -> PrivateAttribute:
  """Marks an attribute as private."""
  return PrivateAttribute(*args, **kwargs)


class PrivateSpace(dict):
  """This class provides privacy aware namespace objects. When
  encountering attributes in a class body that are intended to be kept
  private, the entry is placed in an inner private namespace. The
  metaclass creating the class can then handle attributes differently
  based on privacy.

  To mark an attribute as private, simply use the 'private' function,
  for example:

  class Complex(metaclass=PrivacyRespectinator):
    #  Class implementing private attributes
    x = private(0)
    y = private(1)

    @private
    def area(self, ) -> int:
      return self.x * self.y

    def __init__(self, x: int, y: int) -> None:
      self.x = x
      self.y = y

    def __complex__(self, ) -> complex:
      return self.x + 1j * self.y
  """

  __private_space__ = None

  def __setitem__(self, key: str, value: Any) -> None:
    if not isinstance(value, _Private):
      return dict.__setitem__(self, key, value)
    existing = getattr(self, '__private_space__', {})
    pvtObject = value.__private_object__
    setattr(self, '__private_space__', {**existing, key: pvtObject})

  def compile(self, ) -> dict:
    """Compiles the private space into a dictionary."""
    return {k: v for (k, v) in dict.items(self, )}


class PrivacyRespectinator(type):
  """Allows for private attributes to be actually private."""

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases, **kwargs) -> dict:
    namespace = PrivateSpace()
