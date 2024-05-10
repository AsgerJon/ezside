"""The 'parseFont' function creates instances of QFont. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QFont, QFontDatabase


def parseFont(*args, **kwargs) -> QFont:
  """The 'parseFont' function creates instances of QFont. """
  fontFamilies = QFontDatabase().families()
  family, fontSize, fontWeight, fontCase = None, None, None, None
  for arg in args:
    if isinstance(arg, str):
      if arg in fontFamilies and family is None:
        family = arg
    elif isinstance(arg, int) and fontSize is None:
      fontSize = arg
    elif isinstance(arg, QFont.Weight) and fontWeight is None:
      fontWeight = arg
    elif isinstance(arg, QFont.Capitalization) and fontCase is None:
      fontCase = arg
  family = 'Helvetica' if family is None else family
  fontSize = 12 if fontSize is None else fontSize
  fontWeight = QFont.Weight.Normal if fontWeight is None else fontWeight
  fontCase = QFont.Capitalization.MixedCase if fontCase is None else fontCase
  font = QFont()
  font.setFamily(family)
  font.setPointSize(fontSize)
  font.setWeight(fontWeight)
  font.setCapitalization(fontCase)
  return font
