#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
#
# from typing import Self
#
#
# def classCreated(cls: type) -> type:
#   """Creates a class"""
#   print('\n')
#   print('Finished creating: %s' % cls.__name__)
#   return cls
#
#
# @classCreated
# class MetaTest(type):
#   """MetaTest"""
#
#   @classmethod
#   def __prepare__(mcls, name: str, bases: tuple, **kwargs) -> dict:
#     """__prepare__"""
#     print('MetaTest.__prepare__: %s' % name)
#     return dict(lmao=True)
#
#   def __new__(mcls,
#               name: str,
#               bases: tuple,
#               namespace: dict,
#               **kwargs) -> type:
#     """__new__"""
#     print('MetaTest.__new__: %s' % name)
#     return super().__new__(mcls, name, bases, namespace)
#
#   def __init__(cls,
#                name: str,
#                bases: tuple,
#                namespace: dict,
#                **kwargs) -> None:
#     """__init__"""
#     print('MetaTest.__init__: %s' % name)
#     super().__init__(name, bases, namespace)
#
#   def __call__(cls, *args, **kwargs) -> object:
#     """__call__"""
#     print('MetaTest.__call__: %s' % cls.__name__)
#     return super().__call__(*args, **kwargs)
#
#   def __str__(cls) -> str:
#     """Text explanation"""
#     return cls.__name__
#
#
# @classCreated
# class Field(metaclass=MetaTest):
#   """Field lmao"""
#
#   __slots__ = ['defaultValue', '__field_name__', '__field_owner__']
#   __slot_types__ = {
#     'val'            : int,
#     '__field_name__' : str,
#     '__field_owner__': type}
#
#   def __init__(self, val: int = None) -> None:
#     """LMAO"""
#     self.defaultValue = 0 if val is None else val
#
#   def __set_name__(self, owner: type, name: str) -> None:
#     """__set_name__"""
#     print('Field.__set_name__: owner: %s, name: %s' % (owner, name))
#     self.__field_name__ = name
#     self.__field_owner__ = owner
#
#   def _getPrivateName(self) -> str:
#     """Private name getter"""
#     return '_%s' % self.__field_name__
#
#   def __get__(self, instance: object, owner: type) -> int | Self:
#     """LMAO"""
#     if instance is None:
#       return self
#     pvtName = self._getPrivateName()
#     if not hasattr(instance, pvtName):
#       setattr(instance, pvtName, self.defaultValue)
#     return getattr(instance, pvtName)
#
#   def __set__(self, instance: object, value: int) -> None:
#     """LMAO"""
#     pvtName = self._getPrivateName()
#     setattr(instance, pvtName, value)
#
#   def __str__(self) -> str:
#     """Text explanation"""
#     return self.__field_name__ or object.__str__(self)
#
#
# @classCreated
# class Parent(metaclass=MetaTest):
#   """Parent"""
#
#   x = Field(69)
#   y = Field(420)
#
#   def __init__(self, *args, **kwargs) -> None:
#     """LMAO"""
#     intArgs = [arg for arg in args if isinstance(arg, int)]
#     x, y = [*intArgs, None, None][:2]
#     if y is not None:
#       self.x = x
#       self.y = y
#     elif x is not None:
#       self.x = x
#
#   def __str__(self) -> str:
#     """Text explanation"""
#     clsName = self.__class__.__name__
#     return '%s(x=%d, y=%d)' % (clsName, self.x, self.y)
#
#   def __init_subclass__(cls, **kwargs) -> None:
#     """__init_subclass__"""
#     print('Parent.__init_subclass__: %s' % cls.__name__)
#     print('  - kwargs? : %s' % (str(kwargs),))
#
#
# @classCreated
# class Child(Parent):
#   """Child"""
#
#   z = Field(1337)
#
#   def __init__(self, *args, **kwargs) -> None:
#     """LMAO"""
#     intArgs = [arg for arg in args if isinstance(arg, int)]
#     x, y, z = [*intArgs, None, None, None][:3]
#     if z is not None:
#       self.z = z
#     super().__init__(*args, **kwargs)
#
#   def __str__(self) -> str:
#     """Text explanation"""
#     clsName = self.__class__.__name__
#     return '%s(x=%d, y=%d, z=%d)' % (clsName, self.x, self.y, self.z)
