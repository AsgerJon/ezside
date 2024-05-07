"""AlignBox wraps the Qt.AlignmentFlag enum making it suitable for use as
in AttriBox instances. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtCore import Qt
from vistutils.waitaminute import typeMsg

from ezside.core import Center


class AlignBox:
  """AlignBox wraps the Qt.AlignmentFlag enum making it suitable for use
  in AttriBox instances. """

  __alignment_flag__ = None

  def __init__(self, *args, **kwargs) -> None:
    names = [align.name for align in Qt.AlignmentFlag]
    values = [align.value for align in Qt.AlignmentFlag]
    for arg in args:
      if isinstance(arg, str):
        if arg in names:
          for align in Qt.AlignmentFlag:
            if align.name == arg:
              self.__alignment_flag__ = align
              break
      if isinstance(arg, int):
        if arg in values:
          for align in Qt.AlignmentFlag:
            if align.value == arg:
              self.__alignment_flag__ = align
              break
      if isinstance(arg, Qt.AlignmentFlag):
        self.__alignment_flag__ = arg
        break
    else:
      self.__alignment_flag__ = Center

  def __eq__(self, other: Any) -> bool:
    """Recognizes instances of Qt.AlignmentFlag"""
    if other in Qt.AlignmentFlag:
      return True if self.__alignment_flag__ == other else False
    return NotImplemented

  def __or__(self, other: Any) -> Any:
    """Implementation of the bitwise OR operator."""
    return self.__class__(self.__alignment_flag__ | other)

  def __str__(self, ) -> str:
    """String representation of the instance."""
    return str(self.__alignment_flag__.name)

  __ready_box__ = True
  __outer_box__ = None
  __owning_instance__ = None
  __field_owner__ = None
  __field_name__ = None

  def getFieldOwner(self) -> type:
    """Getter-function for the field owner. """
    return self.__field_owner__

  def setFieldOwner(self, owner: type) -> None:
    """Setter-function for the field owner. """
    if self.__field_owner__ is not None:
      e = """The field owner has already been assigned!"""
      raise AttributeError(e)
    if isinstance(owner, type):
      self.__field_owner__ = owner
    else:
      e = typeMsg('owner', owner, type)
      raise TypeError(e)

  def getFieldName(self) -> str:
    """Getter-function for the field name. """
    return self.__field_name__

  def setFieldName(self, name: str) -> None:
    """Setter-function for the field name. """
    if self.__field_name__ is not None:
      e = """The field name has already been assigned!"""
      raise AttributeError(e)
    if isinstance(name, str):
      self.__field_name__ = name
    else:
      e = typeMsg('name', name, str)
      raise TypeError(e)

  def getOwningInstance(self) -> object:
    """Getter-function for the owning instance. """
    return self.__owning_instance__

  def setOwningInstance(self, instance: object) -> None:
    """Setter-function for the owning instance. """
    if self.__owning_instance__ is not None:
      e = """The owning instance has already been assigned!"""
      raise AttributeError(e)
    self.__owning_instance__ = instance

  def getOuterBox(self, ) -> object:
    """Getter-function for the outer box. """
    return self.__outer_box__

  def setOuterBox(self, box: object) -> None:
    """Setter-function for the outer box. """
    if self.__outer_box__ is not None:
      e = """The outer box has already been assigned!"""
      raise AttributeError(e)
    self.__outer_box__ = box
