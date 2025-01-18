"""FontFamily encapsulates supported font families. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QFont, QFontDatabase

from worktoy.text import monoSpace
from worktoy.desc import THIS, Field
from worktoy.meta import BaseMetaclass
from worktoy.base import overload


class UnsupportedFamilyException(ValueError):
  """UnsupportedFamilyException is raised when the font family is not
  supported."""

  def __init__(self, family: str) -> None:
    """UnsupportedFamilyException is raised when the font family is not
    supported."""
    supportedFonts = QFontDatabase().families()
    fontStr = '<br><tab>'.join(supportedFonts)
    e1 = """The font family: '%s' is not supported by the current 
    application!""" % family
    e2 = """Supported families are: <br><tab>%s""" % fontStr
    ValueError.__init__(self, monoSpace("""%s<br>%s""" % (e1, e2)))


class _MetaFontFamily(BaseMetaclass):
  """MetaFontFamily provides the metaclass for the FontFamily class. """

  def __contains__(self, family: str) -> bool:
    """Returns True if the font family is supported."""
    families = [name.lower() for name in QFontDatabase().families()]
    return True if family.lower() in families else False


class FontFamily(metaclass=_MetaFontFamily):
  """FontFamily encapsulates supported font families. """

  __fallback_name__ = 'MesloLGS NF'
  __family_name__ = None
  name = Field()

  @staticmethod
  def _parseFontFamily(familyName: str, **kwargs) -> str:
    """Parses the font family name."""
    #  Strict
    for fontFamily in QFontDatabase().families():
      if familyName == fontFamily:
        return fontFamily
    #  Case-insensitive
    for fontFamily in QFontDatabase().families():
      if familyName.lower() == fontFamily.lower():
        return fontFamily
    #  Partial match
    for fontFamily in QFontDatabase().families():
      familyParts = fontFamily.lower().split()
      for namePart in familyName.split():
        if namePart.lower() not in familyParts:
          break
      else:
        return fontFamily
    #  Loose partial match
    for fontFamily in QFontDatabase().families():
      familyParts = fontFamily.lower().split()
      for familyPart in familyParts:
        if familyName.lower() in familyPart:
          return fontFamily
    if kwargs.get('strict', True):
      raise UnsupportedFamilyException(familyName)

  @overload(str)
  def __init__(self, family: str) -> None:
    self.__family_name__ = self._parseFontFamily(family)

  @overload(QFont)
  def __init__(self, font: QFont) -> None:
    self.__family_name__ = self._parseFontFamily(font.family())

  @overload(THIS)
  def __init__(self, other: FontFamily) -> None:
    self.__family_name__ = other.name

  @overload()
  def __init__(self) -> None:
    self.__family_name__ = self.__fallback_name__

  @name.GET
  def _getName(self) -> str:
    """Getter-function for the name of the font family. This method also
    performs validation of the name by checking if the currently running
    application instance supports the font family. This step is omitted
    if no application instance is running."""
    if self.__family_name__ is None:
      e = """The font family name is not set. """
      raise RuntimeError(e)
    if self.__family_name__ in self:
      return self.__family_name__

  def __contains__(self, family: str) -> bool:
    """Returns True if the font family is supported."""
    return True if family in type(self) else False

  def __str__(self, ) -> str:
    """String representation of the font family."""
    return """FontFamily: %s""" % self.name

  def __repr__(self, ) -> str:
    """Returns the representation of the font family."""
    clsName = type(self).__name__
    return """%s(%s)""" % (clsName, self.name)
