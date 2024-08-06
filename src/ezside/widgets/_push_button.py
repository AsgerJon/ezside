"""PushButton implementation for the ezside library."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Signal, QPoint
from PySide6.QtGui import QEnterEvent, QMouseEvent
from worktoy.desc import Field

from ezside.widgets import Label, ButtonState


class PushButton(Label):
  """This class provides the state awareness of a push button. """

  #  PRIVATE  # ----------------
  __is_active__ = None
  __under_mouse__ = None
  __mouse_pressed__ = None
  __cursor_position__ = None
  #  PUBLIC  # -----------------
  active = Field()
  underMouse = Field()
  mousePressed = Field()
  buttonState = Field()
  #  Cursor position  # --------
  x = Field()  # int
  y = Field()  # int
  p = Field()  # QPoint
  #  Signals  # ----------------
  mouseLeave = Signal()
  mouseEnter = Signal()
  mousePress = Signal()
  mouseRelease = Signal()

  @active.GET
  def _getActive(self) -> bool:
    """Getter-function for the is_active attribute."""
    return self.__is_active__

  @underMouse.GET
  def _getUnderMouse(self) -> bool:
    """Getter-function for the underMouse attribute."""
    return self.__under_mouse__

  @mousePressed.GET
  def _getMousePressed(self) -> bool:
    """Getter-function for the mousePressed attribute."""
    return self.__mouse_pressed__

  @buttonState.GET
  def _getButtonState(self) -> ButtonState:
    """Getter-function for the button state."""
    if self.__is_active__:
      if self.__under_mouse__:
        if self.__mouse_pressed__:
          return ButtonState.ENABLED_PRESSED
        return ButtonState.ENABLED_HOVER
      return ButtonState.ENABLED_RELEASED
    if self.__under_mouse__:
      if self.__mouse_pressed__:
        return ButtonState.DISABLED_PRESSED
      return ButtonState.DISABLED_HOVER
    return ButtonState.DISABLED_RELEASED

  @x.GET
  def _getX(self) -> int:
    """Getter-function for the x attribute."""
    return self.__cursor_position__.x()

  @y.GET
  def _getY(self) -> int:
    """Getter-function for the y attribute."""
    return self.__cursor_position__.y()

  @p.GET
  def _getP(self) -> QPoint:
    """Getter-function for the p attribute."""
    return self.__cursor_position__

  def enterEvent(self, event: QEnterEvent) -> None:
    """Event handler for when the mouse enters the widget."""
    Label.enterEvent(self, event)
    self.__under_mouse__ = True
    self.__cursor_position__ = event.pos()
    self.mouseEnter.emit()

  def leaveEvent(self, event: QEnterEvent) -> None:
    """Event handler for when the mouse leaves the widget."""
    Label.leaveEvent(self, event)
    self.__under_mouse__ = False
    self.__mouse_pressed__ = False
    self.__cursor_position__ = QPoint(-1, -1)
    self.mouseLeave.emit()

  def mouseMoveEvent(self, event: QMouseEvent) -> None:
    """Event handler for when the mouse moves over the widget."""
    Label.mouseMoveEvent(self, event)
    self.__under_mouse__ = True
    self.__cursor_position__ = event.pos()

  def mousePressEvent(self, event: QMouseEvent) -> None:
    """Event handler for when the mouse is pressed over the widget."""
    Label.mousePressEvent(self, event)
    self.__mouse_pressed__ = True
    self.mousePress.emit()

  def mouseReleaseEvent(self, event: QMouseEvent) -> None:
    """Event handler for when the mouse is released over the widget."""
    Label.mouseReleaseEvent(self, event)
    self.__mouse_pressed__ = False
    self.mouseRelease.emit()
