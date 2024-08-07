"""FontFamily enumerates font families using KeeNum."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Self

from PySide6.QtGui import QFont
from worktoy.desc import Field
from worktoy.keenum import KeeNum, auto


class FontFamily(KeeNum):
  """FontFamily enumerates font families using KeeNum."""

  qt = Field()

  HELVETICA = auto('Helvetica')
  TIMES = auto('Times')
  COURIER = auto('Courier')
  DEJAVU_SANS = auto('DejaVu Sans')
  FREEMONO = auto('FreeMono')
  FREESANS = auto('FreeSans')
  FREESERIF = auto('FreeSerif')
  INCONSOLATA = auto('Inconsolata')
  LIBERATION_MONO = auto('Liberation Mono')
  LIBERATION_SANS = auto('Liberation Sans')
  LIBERATION_SERIF = auto('Liberation Serif')
  LUCIDA = auto('Lucida')
  NOTO_SANS = auto('Noto Sans')
  NOTO_SERIF = auto('Noto Serif')
  UBUNTU = auto('Ubuntu')
  UBUNTU_CONDENSED = auto('Ubuntu Condensed')
  UBUNTU_LIGHT = auto('Ubuntu Light')
  UBUNTU_MONO = auto('Ubuntu Mono')
  MONTSERRAT = auto('Montserrat')

  def apply(self, font: QFont) -> QFont:
    """Apply the font family to the given QFont."""
    font.setFamily(self.value)
    return font

  @qt.GET
  def _getQt(self) -> QFont:
    """Creates an instance of QFont with this family"""
    out = QFont()
    out.setFamily(self.value)
    return out

  @classmethod
  def __class_call__(cls, *args, **kwargs) -> Self:
    """Class-call method for FontFamily"""
    for arg in args:
      if isinstance(arg, QFont):
        arg = arg.family()
      if isinstance(arg, str):
        for item in cls:
          if item.name.lower() == arg.family().lower():
            return item
      if isinstance(arg, cls):
        return arg
      if isinstance(arg, int):
        for item in cls:
          if int(item) == arg:
            return item
    e = """Unable to resolve FontFamily!"""
    raise ValueError(e)
