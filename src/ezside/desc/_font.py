"""Font implements descriptor protocol for QFont."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Optional, Any

from icecream import ic

from ezside.app import EZObject, MissingSettingsError
from ezside.desc import SettingsDescriptor, \
  FontFamilies, \
  fontWeights, \
  FontCap, Weight, Bold, Normal

from PySide6.QtGui import QFont

ic.configureOutput(includeContext=True)


def parseFont(*args, **kwargs) -> Optional[QFont]:
  """Parse the font."""
  family, fontSize, fontCap, fontWeight = None, None, None, None
  for arg in args:
    if isinstance(arg, QFont):
      return arg
  for arg in args:
    if isinstance(arg, str):
      if arg in FontFamilies and family is None:
        family = arg
        continue
      if arg in fontWeights and fontWeight is None:
        fontWeight = arg
        continue
    if isinstance(arg, int):
      if fontSize is None:
        fontSize = arg
        continue
  font = QFont()
  font.setFamily(family)
  font.setPointSize(fontSize)
  if isinstance(fontCap, FontCap):
    font.setCapitalization(fontCap)
  if isinstance(fontWeight, Weight):
    font.setWeight(fontWeight)
  return font


class Font(SettingsDescriptor):
  """Font implements descriptor protocol for QFont."""

  def getContentClass(self) -> type:
    return QFont

  def create(self, instance: EZObject, owner: type, **kwargs) -> QFont:
    """Create the content."""
    ic(self.getArgs())
    font = parseFont(*self.getArgs())
    if isinstance(font, QFont):
      return font
    raise MissingSettingsError(self.__class__.__name__)

  def getFallbackValues(self) -> dict[str, Any]:
    """Returns the fallback values."""
    return {
      'normal/font': parseFont('Montserrat', 12, Normal),
      'header/font': parseFont('Montserrat', 16, Bold),
      'title/font' : parseFont('Montserrat', 20, Bold),
    }
