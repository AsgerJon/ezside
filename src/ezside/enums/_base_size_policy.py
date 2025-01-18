"""BaseSizePolicy enumerates the base size policy options for the QOL app."""
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from enum import EnumType

from PySide6.QtWidgets import QSizePolicy
from worktoy.keenum import auto

from . import AbstractEnum

_Q_MAXIMUM = QSizePolicy.Policy.Maximum
_Q_PREFERRED = QSizePolicy.Policy.Preferred
_Q_EXPANDING = QSizePolicy.Policy.MinimumExpanding


class BaseSizePolicy(AbstractEnum):
  """BaseSizePolicy enumerates the base size policy options for the QOL
  app."""

  @classmethod
  def getQClass(cls) -> EnumType:
    """Returns the Qt version of this enumeration."""
    return QSizePolicy.Policy

  MAX = auto(_Q_MAXIMUM)
  PREFER = auto(_Q_PREFERRED)
  EXPAND = auto(_Q_EXPANDING)
