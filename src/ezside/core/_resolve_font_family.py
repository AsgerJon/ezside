"""The 'resolveFontFamily' function ensures that the given string is the
name of a valid font family. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QFontDatabase


def resolveFontFamily(family: str) -> str:
  """Resolves the font family name"""
  font_families = QFontDatabase().families()

  if family in font_families:
    return family
  elif family == 'monospace':
    return 'Courier'
  elif family == 'serif':
    return 'Times'
  elif family == 'sans-serif':
    return 'Helvetica'
  else:
    return 'Helvetica'  # default font family
