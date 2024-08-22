"""FontCap class for handling font capitalization."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QFont
from worktoy.desc import Field
from worktoy.keenum import KeeNum, auto


class FontCap(KeeNum):
  """FontCap class for handling font capitalization."""

  qt = Field()

  MIX = auto(QFont.Capitalization.MixedCase)
  UP = auto(QFont.Capitalization.AllUppercase)
  LOW = auto(QFont.Capitalization.AllLowercase)
  SMALL = auto(QFont.Capitalization.SmallCaps)
  CAP = auto(QFont.Capitalization.Capitalize)

  def apply(self, font: QFont) -> QFont:
    """Apply the font capitalization to the given QFont."""
    font.setCapitalization(self.qt)
    return font

  @qt.GET
  def _getQt(self, ) -> QFont.Capitalization:
    """Get the QFont.Capitalization value."""
    return self.value
