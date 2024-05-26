"""Font implements descriptor protocol for QFont."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Optional, Any

from icecream import ic
from PySide6.QtGui import QFont, QFontDatabase
from vistutils.fields import EmptyField
from vistutils.parse import maybe
from vistutils.text import monoSpace
from vistutils.waitaminute import typeMsg

from ezside.app import EZObject, MissingSettingsError
from ezside.desc import SettingsDescriptor, Bold, Normal

ic.configureOutput(includeContext=True)


def parseFont(*args, **kwargs) -> Optional[QFont]:
  """Parse the font."""
  family, fontSize, weight = [*args][:3]
  font = QFont()
  font.setFamily(family)
  font.setPointSize(fontSize)
  font.setWeight(Normal)
  return font


class Font(EmptyField):
  """Font implements descriptor protocol for QFont."""

  __field_name__ = None
  __field_owner__ = None

  __fallback_family__ = 'MesloLGS NF'
  __fallback_font_size__ = 12
  __fallback_weight__ = Normal

  __default_family__ = None
  __default_font_size__ = None
  __default_weight__ = None

  @staticmethod
  def _loadFamilies() -> list[str]:
    """Loads list of registered font families."""
    writingSystem = QFontDatabase.WritingSystem.Latin
    return QFontDatabase.families(writingSystem)

  def __init__(self, *args, **kwargs) -> None:
    family, size, weight = None, None, None
    for arg in args:
      if isinstance(arg, str) and family is None:
        family = arg
      if isinstance(arg, int) and size is None:
        size = arg
      if isinstance(arg, QFont.Weight):
        weight = arg
    self.__default_family__ = maybe(family, self.__fallback_family__)
    self.__default_font_size__ = maybe(size, self.__fallback_font_size__)
    self.__default_weight = maybe(weight, self.__fallback_weight__)

  def _createObject(self) -> QFont:
    """Creates an instance of QFont """
    font = QFont()
    font.setFamily(self.__default_family__)
    font.setPointSize(self.__default_font_size__)
    font.setWeight(self.__default_weight)
    return font

  def __set_name__(self, owner: type, name: str) -> None:
    """The __set_name__ method is called when the descriptor is assigned to
    a class attribute. """
    self.__field_name__ = name
    self.__field_owner__ = owner

  def _getFieldName(self) -> str:
    """Getter-functino for field name"""
    return self.__field_name__

  def _getFieldOwner(self) -> type:
    """Getter-function for field owner"""
    return self.__field_owner__

  def _getPrivateName(self) -> str:
    """Getter-function for private name"""
    return '__%s_value__' % (self._getFieldName(),)

  def __get__(self, instance: object, owner: type, **kwargs) -> Any:
    """The __get__ method is called when the descriptor is accessed via the
    owning instance. Subclasses should not override this method, but should
    instead implement the __instance_get__ method. """
    if instance is None:
      return self
    pvtName = self._getPrivateName()
    font = getattr(instance, pvtName, None)
    if font is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      setattr(instance, pvtName, self._createObject())
      return self.__get__(instance, owner, _recursion=True)
    if isinstance(font, QFont):
      return font
    e = typeMsg('font', font, QFont)
    raise TypeError(e)

  def __set__(self, instance: object, value: Any) -> None:
    """The __set__ method is called when the descriptor is assigned a value
    via the owning instance. The default implementation raises an error."""
    pvtName = self._getPrivateName()
    if isinstance(value, QFont):
      return setattr(instance, pvtName, value)
    e = typeMsg('value', value, QFont)
    raise TypeError(e)

  def __delete__(self, instance: object) -> None:
    """Deleter-function for the descriptor."""
    pvtName = self._getPrivateName()
    if getattr(instance, pvtName, None) is not None:
      return delattr(instance, pvtName)
    e = """The instance has no attribute at name: '%s'!"""
    raise AttributeError(monoSpace(e % pvtName))
