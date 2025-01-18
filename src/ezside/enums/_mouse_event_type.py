"""MouseEventType enumerates mouse events."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from enum import EnumType

from PySide6.QtCore import QEvent
from worktoy.keenum import auto

from . import AbstractEnum

_Q_SINGLE_CLICK = QEvent.Type.MouseButtonRelease
_Q_DOUBLE_CLICK = QEvent.Type.MouseButtonRelease
_Q_TRIPLE_CLICK = QEvent.Type.MouseButtonRelease
_Q_SINGLE_PRESS_HOLD = QEvent.Type.MouseButtonPress
_Q_DOUBLE_PRESS_HOLD = QEvent.Type.MouseButtonPress
_Q_TRIPLE_PRESS_HOLD = QEvent.Type.MouseButtonPress
_Q_WHEEL = QEvent.Type.Wheel
_Q_ENTER = QEvent.Type.Enter
_Q_LEAVE = QEvent.Type.Leave


class MouseEventType(AbstractEnum):
  """MouseEventType enumerates mouse events."""

  @classmethod
  def getQClass(cls) -> EnumType:
    """Returns the Qt version of this enumeration."""
    return QEvent.Type

  SINGLE_CLICK = auto(_Q_SINGLE_CLICK)
  DOUBLE_CLICK = auto(_Q_DOUBLE_CLICK)
  TRIPLE_CLICK = auto(_Q_TRIPLE_CLICK)
  SINGLE_PRESS_HOLD = auto(_Q_SINGLE_PRESS_HOLD)
  DOUBLE_PRESS_HOLD = auto(_Q_DOUBLE_PRESS_HOLD)
  TRIPLE_PRESS_HOLD = auto(_Q_TRIPLE_PRESS_HOLD)
  WHEEL = auto(_Q_WHEEL)
  ENTER = auto(_Q_ENTER)
  LEAVE = auto(_Q_LEAVE)
