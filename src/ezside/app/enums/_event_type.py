"""EventType enumerates event types. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from enum import EnumType

from PySide6.QtCore import Qt, QEvent
from worktoy.keenum import auto
from . import AbstractEnum

_Q_PAINT = QEvent.Type.Paint
_Q_MOVE = QEvent.Type.Move
_Q_RESIZE = QEvent.Type.Resize
_Q_INPUT = QEvent.Type.InputMethod


class EventType(AbstractEnum):
  """EventType enumerates event types. """

  @classmethod
  def getQClass(cls) -> EnumType:
    """Returns the Qt version of this enumeration."""
    return QEvent.Type

  PAINT = auto(_Q_PAINT)
  MOVE = auto(_Q_MOVE)
  RESIZE = auto(_Q_RESIZE)
  INPUT = auto(_Q_INPUT)
