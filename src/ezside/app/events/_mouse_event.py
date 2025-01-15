"""MouseEvent encapsulates user input event from a mouse. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from PySide6.QtCore import QPointF
from PySide6.QtGui import QVector2D, QMouseEvent, QEventPoint
from PySide6.QtGui import QSinglePointEvent
from worktoy.desc import Field
from worktoy.base import BaseObject
from worktoy.text import typeMsg

from ..core import Vector2D
from ..enums import MouseButton, KeyMod


class MouseEvent(BaseObject):
  """MouseEvent encapsulates user input event from a mouse. """

  __event_point__ = None
  __time_duration__ = None
  __move_vector__ = None
  __velocity_vector__ = None
  __mouse_button__ = None
  __key_mod__ = None

  duration = Field()
  move = Field()
  velocity = Field()
  button = Field()
  keyMod = Field()

  drift = Field()
  speed = Field()
  SHIFT = Field()
  CTRL = Field()
  ALT = Field()
  META = Field()

  TYPE = Field()

  @staticmethod
  def _resolveEventPoint(event: QMouseEvent) -> QEventPoint:
    eventPoints = QSinglePointEvent.points(event)
    if len(eventPoints) == 1:
      return eventPoints[0]
    if eventPoints:
      e = """Multiple event points found in QMouseEvent!"""
      raise RuntimeError(e)
    e = """No event points found in QMouseEvent!"""
    raise RuntimeError(e)

  def __init__(self, event: QMouseEvent) -> None:
    """MouseRelease is initialized with a QMouseEvent. """
    p = self._resolveEventPoint(event)
    self.__time_duration__ = p.timestamp() - p.lastTimestamp()
    self.__move_vector__ = Vector2D(p)
    self.__velocity_vector__ = Vector2D(p.velocity())
    self.__mouse_button__ = MouseButton(event.button())
    self.__key_mod__ = KeyMod(event.modifiers())
    self.__event_type__ = event.type()

  @duration.GET
  def _getDuration(self) -> int:
    """Getter-function for the duration of the event. """
    if self.__time_duration__ is None:
      e = """No duration has been set for this event!"""
      raise RuntimeError(e)
    if isinstance(self.__time_duration__, int):
      return self.__time_duration__
    e = typeMsg('__time_duration__', self.__time_duration__, int)
    raise TypeError(e)

  @move.GET
  def _getMove(self) -> Vector2D:
    """Getter-function for the move vector of the event. """
    if self.__move_vector__ is None:
      e = """No move vector has been set for this event!"""
      raise RuntimeError(e)
    if isinstance(self.__move_vector__, Vector2D):
      return self.__move_vector__
    e = typeMsg('__move_vector__', self.__move_vector__, Vector2D)
    raise TypeError(e)

  @velocity.GET
  def _getVelocity(self) -> Vector2D:
    """Getter-function for the velocity vector of the event. """
    if self.__velocity_vector__ is None:
      e = """No velocity vector has been set for this event!"""
      raise RuntimeError(e)
    if isinstance(self.__velocity_vector__, Vector2D):
      return self.__velocity_vector__
    e = typeMsg('__velocity_vector__', self.__velocity_vector__, Vector2D)
    raise TypeError(e)

  @button.GET
  def _getButton(self) -> MouseButton:
    """Getter-function for the mouse button of the event. """
    if self.__mouse_button__ is None:
      e = """No mouse button has been set for this event!"""
      raise RuntimeError(e)
    if isinstance(self.__mouse_button__, MouseButton):
      return self.__mouse_button__
    e = typeMsg('__mouse_button__', self.__mouse_button__, MouseButton)
    raise TypeError(e)

  @keyMod.GET
  def _getKeyMod(self) -> KeyMod:
    """Getter-function for the key modifiers of the event. """
    if self.__key_mod__ is None:
      e = """No key modifiers have been set for this event!"""
      raise RuntimeError(e)
    if isinstance(self.__key_mod__, KeyMod):
      return self.__key_mod__
    e = typeMsg('__key_mod__', self.__key_mod__, KeyMod)
    raise TypeError(e)

  @speed.GET
  def _getSpeed(self) -> float:
    if TYPE_CHECKING:
      assert isinstance(self.velocity, QVector2D)
    return self.velocity.length()

  @drift.GET
  def _getDrift(self) -> float:
    if TYPE_CHECKING:
      assert isinstance(self.move, QVector2D)
    return self.move.length()

  @TYPE.GET
  def _getType(self) -> Any:
    return self.__event_type__
