"""PushButton provides a push button widget by subclassing the Label
widget and adding state awareness and signal/slot connections."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import time

from PySide6.QtCore import Signal, QEvent
from PySide6.QtGui import QEnterEvent, QMouseEvent
from attribox import AttriBox

from ezside.core import EZTimer
from ezside.widgets import Label


class PushButton(Label):
  """PushButton provides a push button widget by subclassing the Label
  widget and adding state awareness and signal/slot connections."""

  __waiting_release__ = False
  __under_mouse__ = False
  __press_position__ = None
  __move_time__ = None
  __mouse_speed__ = None

  clicked = Signal()
  pressHold = Signal()

  releaseTimer = AttriBox[EZTimer](500)
  pressReleaseTimer = AttriBox[EZTimer](750)

  def __init__(self, *args, **kwargs) -> None:
    Label.__init__(self, *args, **kwargs)
    self.setMouseTracking(True)

  def initSignalSlot(self) -> None:
    """Initializes the signal/slot connections for the push button."""
    self.releaseTimer.timeout.connect(self._cancelClick)
    self.pressReleaseTimer.timeout.connect(self.pressHold.emit)

  def _getMouseSpeed(self) -> float:
    """Getter-function for mouse speed"""
    if self.__mouse_speed__ is None:
      self.__mouse_speed__ = 0
    return self.__mouse_speed__

  def _setMouseSpeed(self, speed: float) -> None:
    """Setter-function for mouse speed"""
    self.__mouse_speed__ = speed

  def _cancelClick(self, ) -> None:
    """Cancels the click signal."""
    self.__waiting_release__ = False

  def _getMoveTime(self) -> float:
    """Getter-function for move time"""
    if self.__move_time__ is None:
      self.__move_time__ = time.time() + 10
    return self.__move_time__

  def _setMoveTime(self, when: float) -> None:
    """Setter-function for move time"""
    self.__move_time__ = when

  def leaveEvent(self, event: QEvent) -> None:
    """Handles the leave event."""
    self.__waiting_release__ = False
    self.releaseTimer.stop()
    self.pressReleaseTimer.stop()
    self.__under_mouse__ = False
    Label.leaveEvent(self, event)

  def enterEvent(self, event: QEnterEvent) -> None:
    """Handles the enter event."""
    self.__under_mouse__ = True
    Label.enterEvent(self, event)

  def mouseReleaseEvent(self, event: QMouseEvent) -> None:
    """Handles the mouse release event."""
    if self.__waiting_release__ and self.__under_mouse__:
      self.clicked.emit()
      self.__waiting_release__ = False
      self.releaseTimer.stop()
    self.pressReleaseTimer.stop()
    Label.mouseReleaseEvent(self, event)

  def mousePressEvent(self, event: QMouseEvent) -> None:
    """Handles the mouse press event."""
    self.__press_position__ = event.pos()
    self.__waiting_release__ = True
    self.releaseTimer.start()
    self.pressReleaseTimer.start()
    Label.mousePressEvent(self, event)

  def mouseMoveEvent(self, event: QMouseEvent) -> None:
    """Handles the mouse move event."""
    here = event.pos()
    there = self.__press_position__
    squareDist = (here.x() - there.x()) ** 2 + (here.y() - there.y()) ** 2
    drift = self.getStyle('maxMove', 8)
    if squareDist > drift ** 2:
      self.__waiting_release__ = False
      self.releaseTimer.stop()
      self.pressReleaseTimer.stop()
    then = self._getMoveTime()
    now = time.time()
    epoch = now - then
    if epoch > 0:
      self._setMouseSpeed(drift ** 0.5 / (now - then))
    self._setMoveTime(now)

  def getState(self, ) -> str:
    """Returns the state of the push button."""
    if self.__waiting_release__:
      return 'pressed'
    if self.__under_mouse__:
      return 'hovered'
    return 'normal'
