"""FontWeight enumerates font weights using KeeNum."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QFont
from worktoy.desc import Field
from worktoy.keenum import KeeNum, auto


class FontWeight(KeeNum):
  """FontWeight enumerates font weights using KeeNum."""

  qt = Field()

  LIGHT = auto(QFont.Weight.Thin)
  NORMAL = auto(QFont.Weight.Normal)
  BOLD = auto(QFont.Weight.Bold)

  def apply(self, font: QFont) -> QFont:
    """Apply the font weight to the given QFont."""
    font.setWeight(self.qt)
    return font

  @qt.GET
  def _getQt(self) -> QFont.Weight:
    """Get the QFont.Weight value."""
    return self.value
