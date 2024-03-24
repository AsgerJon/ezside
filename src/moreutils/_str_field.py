"""StrField provides a strongly typed descriptor field for strings"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from vistutils.parse import maybe
from vistutils.text import monoSpace
from vistutils.waitaminute import typeMsg


class StrField:
  """StrField provides a strongly typed descriptor field for strings"""
  __field_name__ = None
  __field_owner__ = None
  __fallback_value__ = ''
  __default_value__ = None

  def __init__(self, defVal: str = None) -> None:
    text = maybe(defVal, self.__fallback_value__)
    if isinstance(text, str):
      self.__default_value__ = text
    else:
      e = typeMsg('defVal', defVal, str)
      raise TypeError(e)

  def __set_name__(self, owner: type, name: str) -> None:
    self.__field_name__ = name
    self.__field_owner__ = owner

  def getDefaultValue(self) -> str:
    """Getter-function for the default value"""
    return self.__default_value__

  def getFieldOwner(self) -> type:
    """Getter-function for the field owner"""
    if self.__field_owner__ is not None:
      if isinstance(self.__field_owner__, type):
        return self.__field_owner__
      e = typeMsg('self.__field_owner__', self.__field_owner__, type)
      raise TypeError(e)
    e = """Instances of StrField, and descriptors in general, will not 
    have their field name populated until their owning class is actually 
    created. During the execution of the owning class body, objects are 
    created and are placed in the namespace object created by the 
    metaclass (normally type which uses a plain 'dict' object). This error 
    indicates an attempt has been made to access the field name before the 
    metaclass has finished creating the owning class. """
    raise AttributeError(monoSpace(e))

  def getFieldName(self) -> str:
    """Getter-function for the private field name"""
    if self.__field_name__ is not None:
      if isinstance(self.__field_name__, str):
        return self.__field_name__
      e = typeMsg('self.__field_name__', self.__field_name__, str)
      raise TypeError(e)
    e = """Instances of StrField, and descriptors in general, will not 
    have their field name populated until their owning class is actually 
    created. During the execution of the owning class body, objects are 
    created and are placed in the namespace object created by the 
    metaclass (normally type which uses a plain 'dict' object). This error 
    indicates an attempt has been made to access the field name before the 
    metaclass has finished creating the owning class. """
    raise AttributeError(monoSpace(e))

  def _getPrivateFieldName(self, ) -> str:
    """Getter-function for the private field name"""
    return '_%s' % self.getFieldName()

  def __get__(self, instance: object, owner: type, **kwargs) -> Any:
    """Implementation of the getter function for the descriptor"""
    if instance is None:
      return self
    pvtName = self._getPrivateFieldName()
    if getattr(instance, pvtName, None) is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      setattr(instance, pvtName, self.getDefaultValue())
      return self.__get__(instance, owner, _recursion=True)
    return getattr(instance, pvtName)

  def __set__(self, instance: object, value: str) -> None:
    """Implementation of the setter function for the descriptor"""
    if isinstance(value, str):
      pvtName = self._getPrivateFieldName()
      return setattr(instance, pvtName, value)
    e = typeMsg('value', value, str)
    raise TypeError(e)

  def __delete__(self, instance: object) -> None:
    """Implementation of the deleter function for the descriptor"""
    pvtName = self._getPrivateFieldName()
    if hasattr(instance, pvtName):
      return delattr(instance, pvtName)
    e = """No attribute found at name: '%s'""" % (pvtName,)
    raise AttributeError(monoSpace(e))

  def __str__(self, ) -> str:
    """Implementation of the string function for the descriptor"""
    try:
      fieldName = self.getFieldName()
      ownerName = self.getFieldOwner()
      return '%s.%s' % (ownerName, fieldName)
    except AttributeError as attributeError:
      if 'During the execution of the owning class ' in str(attributeError):
        return object.__str__(self)
      raise attributeError

  def __repr__(self, ) -> str:
    """Implementation of the representation function for the descriptor"""
    clsName = self.__class__.__name__
    if self.__default_value__ == self.__fallback_value__:
      return '%s()' % clsName
    defVal = self.getDefaultValue()
    return '%s(%s)' % (clsName, defVal)
