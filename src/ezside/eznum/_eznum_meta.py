"""EnumMeta class for the EZNum base class"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Callable, Any

from icecream import ic
from vistutils.text import monoSpace
from eznum import auto


class EZnumMeta(type):
  """EnumMeta provides the metaclass for the LayoutEnum."""

  @classmethod
  def __prepare__(mcls, name: str, bases: tuple[type], **kwargs) -> dict:
    """Returns the namespace."""
    bases = [b for b in bases if b.__class__ is not mcls]
    if not bases:
      return {}
    if len(bases) == 1 and bases[0] is object:
      return {}
    e = """EZnum classes do not support base classes, but received: <br>%s"""
    e2 = '<br><tab>'.join([str(b) for b in bases])
    raise TypeError(monoSpace(e % e2))

  @classmethod
  def _getAttrFactory(cls) -> Callable:
    """Returns the attribute factory."""

    def __getattr__(self, name: str) -> Any:
      """Returns the attribute."""
      try:
        return object.__getattribute__(self, name.lower())
      except AttributeError as attributeError:
        raise attributeError from AttributeError(name)

    return __getattr__

  @staticmethod
  def getBaseNameSpace() -> dict:
    """Returns the base namespace."""
    return {'name'                   : None, 'value': None,
            '__annotations__'        : {'name': str, 'value': int},
            '__members__'            : None,
            '__allow_instantiation__': True,
            '__iter_contents__'      : None, }

  @classmethod
  def _strFactory(mcls) -> Callable:
    """Returns the string representation of the class."""

    def __str__(self, ) -> str:
      """Returns the string representation of the class."""
      return self.name

    return __str__

  @classmethod
  def _reprFactory(mcls) -> Callable:
    """Returns the string representation of the class."""

    def __repr__(self, ) -> str:
      """Returns the string representation of the class."""
      clsName = self.__class__.__qualname__
      return '%s.%s' % (clsName, self.name,)

    return __repr__

  def __new__(mcls,
              name: str,
              bases: tuple[type],
              namespace: dict,
              **kwargs) -> type:
    enums = [k for (k, v) in namespace.items() if isinstance(v, auto)]
    enumSpace = {}
    coreSpace = dict(__name__=name,
                     __metaclass__=mcls,
                     __str__=mcls._strFactory(),
                     __repr__=mcls._reprFactory(),
                     __getattr__=mcls._getAttrFactory(), )
    baseSpace = mcls.getBaseNameSpace() | coreSpace
    cls = type.__new__(mcls, name, (), baseSpace)

    members = {}
    for (i, name) in enumerate(enums):
      enum = cls()
      setattr(enum, 'name', name)
      setattr(enum, 'value', i)
      setattr(cls, name, enum)
      members[name] = enum
    setattr(cls, '__members__', members)
    setattr(cls, '__allow_instantiation__', False)
    return cls

  def __init__(cls,
               name_: str,
               bases: tuple[type],
               namespace: dict,
               **kwargs) -> None:
    for (name, enum) in getattr(cls, '__members__').items():
      if name.lower() != name:
        setattr(cls, name.lower(), enum)
      if name.upper() != name:
        setattr(cls, name.upper(), enum)
    type.__init__(cls, name_, bases, namespace, **kwargs)

  def __iter__(cls) -> type:
    """Iterates through the members."""
    m = getattr(cls, '__members__', )
    setattr(cls, '__iter_contents__', [v for (k, v) in m.items()])
    return cls

  def __next__(cls) -> type:
    """Iterates through the members."""
    i = getattr(cls, '__iter_contents__', )
    try:
      value = i.pop(0)
      setattr(cls, '__iter_contents__', i)
      return value
    except IndexError:
      setattr(cls, '__iter_contents__', None)
      raise StopIteration

  def __str__(cls, ) -> str:
    """Returns the string representation of the class."""
    return cls.__name__

  def _lookUp(cls, name: str, **kwargs) -> Any:
    """Returns the enum member."""
    members = getattr(cls, '__members__')
    if name in members:
      return members[name]
    if name != name.lower():
      if name.lower() in members:
        return members[name.lower()]
    if name != name.upper():
      if name.upper() in members:
        return members[name.upper()]
    if kwargs.get('_recursion', True):
      val = kwargs.get('_recursion', 2)
      if not val:
        e = """Recursion limit reached!"""
        raise RecursionError(e)
      return cls._lookUp(name.lower(), )
    try:
      cls._lookUp(name.lower())
    except NameError as nameError:
      try:
        cls._lookUp(name.upper())
      except NameError as nameError3:
        raise nameError3
      e = """'%s' is not a member of the %s class."""
      raise NameError(e % (name, cls.__name__)) from nameError
    e = """'%s' is not a member of the %s class."""
    raise NameError(e % (name, cls.__name__))

  def __call__(cls, *args, **kwargs) -> Any:
    """Returns the enum member."""
    if not args and not kwargs:
      return type.__call__(cls, )
    if getattr(cls, '__allow_instantiation__', False):
      try:
        return cls._lookUp(args[0])
      except NameError as nameError:
        e = """Enum classes should not be manually instantiated!"""
        raise TypeError(e) from nameError
    return type.__call__(cls, *args, **kwargs)

  def __getitem__(cls, name: str) -> Any:
    """Returns the enum member."""
    if name in getattr(cls, '__members__', ).values():
      return name
    try:
      return cls._lookUp(name)
    except NameError as nameError:
      raise KeyError(name) from nameError

  def __contains__(cls, item: Any) -> bool:
    """Returns True if the name is a member."""
    for (key, val) in getattr(cls, '__members__', ).items():
      if item in [key, val]:
        return True
    return False


class _object(object):
  """_object provides the base class for the EZnum class."""

  def __init_subclass__(cls, **kwargs) -> None:
    """Initializes the subclass."""
    object.__init_subclass__()

  def __init__(self, *args, **kwargs) -> None:
    """We don't need keyword argument errors!"""
    object.__init__(self)


class EZnum(metaclass=EZnumMeta, _root=True):
  """Subclass EZnum instead of setting the metaclass. """

  def __init_subclass__(cls, **kwargs) -> None:
    """We don't need keyword argument errors!"""
    object.__init_subclass__()

  def __init__(self, *args, **kwargs) -> None:
    """We don't need keyword argument errors!"""
    object.__init__(self)

  def __get_attr__(self, name: str) -> Any:
    """Returns the attribute."""
    try:
      return object.__getattribute__(self, name.lower())
    except AttributeError as attributeError:
      raise attributeError from AttributeError(name)
