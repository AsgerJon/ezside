"""AbstractEnum provides an abstract baseclass for enumerations of the
application. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from enum import EnumType
from typing import Any, TYPE_CHECKING, Self

from PySide6.QtCore import Qt
from worktoy.text import monoSpace
from worktoy.desc import Field
from worktoy.keenum import KeeNum, auto, MetaNum


class _MetaAbstractEnum(MetaNum):
  """Expands the MetaNum metaclass such that members can be resolved from
  their Q version counterparts. """

  def _resolveNum(cls, identifier: Any) -> Any:
    """Now includes support for resolving members from their Q version"""
    if isinstance(type(identifier), EnumType):
      for member in cls:
        if member.value == identifier:
          return member
    return MetaNum._resolveNum(cls, identifier)

  def fromQ(cls, qVal: Any) -> Self:
    """Resolves the enumeration member from its Q version."""
    try:
      for member in cls:
        if member.Q == qVal:
          return member
    except NotImplementedError:
      e = """The enum: '%s' does not support resolution from Q based 
      values!""" % cls.__name__
      raise TypeError(monoSpace(e))
    e = """Unable to resolve value: '%s' as a member of '%s'!"""
    clsName = cls.__name__
    raise ValueError(monoSpace(e % (str(qVal), clsName)))


class AbstractEnum(KeeNum, metaclass=_MetaAbstractEnum):
  """AbstractEnum provides an abstract baseclass for enumerations of the
  application. """

  Q = Field()

  @classmethod
  def getQClass(cls) -> Any:
    """Subclasses may implement this method to specify the Q EnumType that
    corresponds to this enumeration. The purpose of this method is to
    allow the metaclass to resolve members uniquely from their Q version.
    If this is not appropriate for a particular subclass, for example one
    whose members cannot be uniquely resolved from a Q EnumType, then the
    default implementation, which raises a TypeError may be kept. """
    if TYPE_CHECKING:
      return Qt.ReturnByValueConstant  # Dummy return type
    e = """The class: %s does not allow resolution of members from their Q
    EnumType!""" % cls.__name__
    raise TypeError(monoSpace(e))

  def __str__(self, ) -> str:
    selfName = self.name.capitalize()
    clsName = self.__class__.__name__
    return """%s.%s""" % (clsName, selfName)

  @Q.GET
  def _getQVersion(self, ) -> EnumType:
    """Returns the Qt version of this enumeration."""
    return self.value

  def __getattr__(self, name: str) -> Any:
    cls = type(self)
    try:
      for member in cls:  # TypeError indicates that cls is not iterable
        if member.name.lower() == name.lower():
          return member
      raise NameError(name)
    except TypeError as typeError:
      e = """Class '%s' is not iterable!""" % cls.__name__
      raise TypeError(e) from typeError
    except NameError:  # The normal AttributeError is allowed to be raised
      return object.__getattribute__(self, name)
