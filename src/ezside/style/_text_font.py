"""TextFont encapsulates text font in a data class"""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QFont, Qt


class TextFont:
  """TextFont encapsulates text font in a data class"""

  family: str
  size: int
  weight: int = None

  def _getWeight(self) -> QFont.Weight:
    """Return the weight of the font."""
    for name, value in QFont.Weight.__members__.items():
      if (int(value) - self.weight) ** 2 <= 50 ** 2:
        return value

  def getQFont(self) -> QFont:
    """Return a QFont object."""
    font = QFont()
    font.setFamily(self.family)
    font.setPointSize(self.size)
    font.setWeight(self._getWeight())
    return font
