"""ButtonStates instances enumerate different states of a button."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from enum import Enum
from typing import Any

from PySide6.QtCore import QEvent, QMargins, Signal, QPointF
from PySide6.QtGui import QMouseEvent, QEnterEvent, QColor, QFontMetrics
from attribox import AbstractDescriptor
from icecream import ic

from ezside.core import Precise, AlignFlag, Click, CursorVector, NoClick
from ezside.core import parseBrush, SolidFill, Tight, EZTimer, AlignHCenter
from ezside.widgets import Label

ic.configureOutput(includeContext=True)


class StaticState(Enum):
  """StaticState describes the possible states of a widget that can change
  at runtime, but which are not dependent on user interaction. """
  DISABLED = -1
  NORMAL = 0
  CHECKED = 1

  def __str__(self, ) -> str:
    """String representation"""
    return self.name

  def __repr__(self, ) -> str:
    """String representation"""
    return '%s.%s' % (self.__class__.__name__, self.name)


class DynamicState(Enum):
  """DynamicState describes the possible states of a widget relative to
  immediate user input, such as hover or pressed. """
  NORMAL = 0
  HOVER = 1
  PRESSED = 2
  MOVING = 3

  def __str__(self, ) -> str:
    """String representation"""
    return self.name

  def __repr__(self, ) -> str:
    """String representation"""
    return '%s.%s' % (self.__class__.__name__, self.name)


class Flag(AbstractDescriptor):
  """Flag provides a boolean valued descriptor class"""

  def __instance_get__(self, instance: object, owner: type) -> Any:
    """Generalized getter-function"""
    if instance is None:
      return self
    pvtName = self._getPrivateName()

  __default_value__ = None

  def __init__(self, defVal: Any) -> None:
    self.__default_value__ = True if defVal else False


class ButtonState:
  """ButtonState describes the possible states of a button."""
