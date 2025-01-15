"""MouseRelease encapsulates a mouse release event. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, Self

from PySide6.QtCore import QPointF, QEvent, Qt
from PySide6.QtGui import QVector2D, QMouseEvent, QEventPoint
from worktoy.desc import AttriBox, Field, THIS
from worktoy.base import BaseObject, overload
from worktoy.text import typeMsg, monoSpace

from ..core import Point, Vector2D
from ..enums import MouseButton


class MouseRelease(BaseObject):
  """MouseRelease encapsulates a mouse release event. """

  duration = AttriBox[int]()
  move = AttriBox[QPointF]()
  velocity = AttriBox[QVector2D]()
  button = AttriBox[MouseButton]()

  CTRL = AttriBox[bool]()
  SHIFT = AttriBox[bool]()
  ALT = AttriBox[bool]()
  META = AttriBox[bool]()

  drift = Field()
  speed = Field()

  def __init__(self, event: QMouseEvent) -> None:
    """MouseRelease is initialized with a QMouseEvent. """
    super().__init__()
    self.duration = event.timestamp()
    self.move = Point(event)
    self.velocity = Vector2D(event.velocity())
    self.button = MouseButton(event.button())
    self.CTRL = event.modifiers() & Qt.KeyboardModifier.ControlModifier
    self.SHIFT = event.modifiers() & Qt.KeyboardModifier.ShiftModifier
    self.ALT = event.modifiers() & Qt.KeyboardModifier.AltModifier
    self.META = event.modifiers() & Qt.KeyboardModifier.MetaModifier

  @speed.GET
  def _getSpeed(self) -> float:
    return self.velocity.length()

  @drift.GET
  def _getDrift(self) -> float:
    x, y = self.move.x(), self.move.y()
    return (x ** 2 + y ** 2) ** 0.5

  def __str__(self, ) -> str:
    fmtSpec = """MouseRelease: moved %.3f in %d ms"""
    return fmtSpec % (self.drift, self.duration)
