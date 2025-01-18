"""HorizontalAlign enumerates the horizontal alignment options for the QOL
app."""
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from enum import EnumType
from PySide6.QtCore import Qt
from worktoy.keenum import auto

from . import AbstractEnum


class HorizontalAlign(AbstractEnum):
  """Enumerates the horizontal alignment options for the QOL app."""

  @classmethod
  def getQClass(cls) -> EnumType:
    """Returns the Qt version of this enumeration."""
    return Qt.AlignmentFlag

  LEFT = auto(Qt.AlignmentFlag.AlignLeft)
  CENTER = auto(Qt.AlignmentFlag.AlignCenter)
  RIGHT = auto(Qt.AlignmentFlag.AlignRight)
