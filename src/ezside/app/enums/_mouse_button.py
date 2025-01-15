"""MouseButton enumerates the common mouse buttons. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from enum import EnumType
from PySide6.QtCore import Qt
from worktoy.keenum import auto

from . import AbstractEnum

_Q_LEFT = Qt.MouseButton.LeftButton
_Q_MIDDLE = Qt.MouseButton.MiddleButton
_Q_RIGHT = Qt.MouseButton.RightButton
_Q_BACKWARD = Qt.MouseButton.BackButton
_Q_FORWARD = Qt.MouseButton.ForwardButton


class MouseButton(AbstractEnum):
  """MouseButton enumerates the common mouse buttons. """

  @classmethod
  def getQClass(cls) -> EnumType:
    """Returns the Qt version of this enumeration."""
    return Qt.MouseButton

  NULL = auto(Qt.MouseButton.NoButton)
  LEFT = auto(_Q_LEFT)
  MIDDLE = auto(_Q_MIDDLE)
  RIGHT = auto(_Q_RIGHT)
  BACKWARD = auto(_Q_BACKWARD)
  FORWARD = auto(_Q_FORWARD)
