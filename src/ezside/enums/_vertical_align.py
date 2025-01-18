"""VerticalAlign enumerates the vertical alignment options for the QOL
app."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from enum import EnumType

from PySide6.QtCore import Qt
from worktoy.keenum import auto

from . import AbstractEnum


class VerticalAlign(AbstractEnum):
  """VerticalAlign enumerates the vertical alignment options for the QOL
  app."""

  @classmethod
  def getQClass(cls) -> EnumType:
    """Returns the Qt version of this enumeration."""
    return Qt.AlignmentFlag

  TOP = auto(Qt.AlignmentFlag.AlignTop)
  CENTER = auto(Qt.AlignmentFlag.AlignVCenter)
  BOTTOM = auto(Qt.AlignmentFlag.AlignBottom)
