"""BaseButton provides button widgets with mouse awareness. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import TypeAlias, Union

from PySide6.QtCore import QRect, QEvent, QTimer, Slot, QSizeF
from PySide6.QtGui import (QPointerEvent, QVector2D,
                           QEventPoint)
from PySide6.QtCore import QRectF, QPoint, Qt, Signal, QPointF
from PySide6.QtGui import QMouseEvent
from icecream import ic
from worktoy.desc import Field
from worktoy.parse import maybe
from worktoy.text import typeMsg

from ezside.tools import ButtonState, Align, MouseTimer, ControlData
from ezside.base_widgets import LayoutWidget

ic.configureOutput(includeContext=True)

Rect: TypeAlias = Union[QRect, QRectF]


class BaseButton(LayoutWidget):
  """BaseButton provides button widgets with mouse awareness. """

  #  Timer settings from JSON
  __control_data__ = None
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Cursor movement
  __cursor_position__ = None
  __mouse_velocity__ = None
  #  Mouse state-flags
  __is_enabled__ = True
  __mouse_pressed__ = None
  __press_event__ = None
  __hold_event__ = None
  #  Mouse-timers
  __single_click_limit__ = None
  __single_press_hold_limit__ = None
  __single_release_click_delay__ = None
  __double_click_limit__ = None
  __double_press_hold_limit__ = None
  __double_release_click_delay__ = None
  __triple_click_limit__ = None
  __triple_press_hold_limit__ = None
  #  Mouse-limit values
  __click_drift__ = None
  __multi_drift__ = None
  __rest_speed__ = None
  __rest_radius__ = None
  __rest_delay__ = None
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Descriptor fields
  #  Flags
  active = Field()
  mousePressed = Field()
  pressedButton = Field()
  #  Button-state
  buttonState = Field()
  controlData = Field()
  #  Cursor movement
  cursorPosition = Field()
  cursorVelocity = Field()
  #  Stored events
  pressEvent = Field()
  holdEvent = Field()
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Signals
  #  Mouse movements
  mouseLeave = Signal()
  mouseEnter = Signal()
  #  Button state changes
  mousePress = Signal()
  mouseRelease = Signal()
  #  Advanced Button Signals
  singleClick = Signal(QPointerEvent)
  doubleClick = Signal(QPointerEvent)
  tripleClick = Signal(QPointerEvent)
  singleHold = Signal(QPointerEvent)
  doubleHold = Signal(QPointerEvent)
  tripleHold = Signal(QPointerEvent)
  restFocus = Signal(QPointerEvent)
  #  Mouse velocity
  moveSpeed = Signal(float)

  #  Accessor functions
  @cursorVelocity.GET
  def _getCursorVelocity(self) -> QVector2D:
    """Getter-function for the cursor velocity."""
    if self.__mouse_velocity__ is None:
      return QVector2D(QPointF(0, 0))
    if isinstance(self.__mouse_velocity__, QVector2D):
      return self.__mouse_velocity__
    e = typeMsg('cursorVelocity', self.__mouse_velocity__, QVector2D)
    raise TypeError(e)

  @cursorPosition.GET
  def _getCursorPosition(self) -> QPointF:
    """Getter-function for the cursor position."""
    if self.__cursor_position__ is None:
      return QPointF(-1, -1)
    if isinstance(self.__cursor_position__, QPoint):
      return QPoint.toPointF(self.__cursor_position__)
    if isinstance(self.__cursor_position__, QPointF):
      return self.__cursor_position__
    e = typeMsg('cursorPosition', self.__cursor_position__, QPointF)
    raise TypeError(e)

  @buttonState.GET
  def _getButtonState(self) -> ButtonState:
    """Getter-function for the button state."""
    if not self.active:
      if self.mousePressed:
        return ButtonState.DISABLED_PRESSED
      if self.underMouse:
        return ButtonState.DISABLED_HOVER
      return ButtonState.DISABLED_RELEASED
    if self.mousePressed:
      return ButtonState.ENABLED_PRESSED
    if self.underMouse:
      return ButtonState.ENABLED_HOVER
    return ButtonState.ENABLED_RELEASED

  @pressedButton.GET
  def _getPressedButton(self) -> Qt.MouseButton:
    """Getter-function for the most recently pressed button"""
    return maybe(self.__pressed_button__, Qt.MouseButton.NoButton)

  @pressedButton.SET
  def _setPressedButton(self, mouseButton: Qt.MouseButton) -> None:
    """Setter-function for the most recently pressed button"""
    self.__pressed_button__ = mouseButton

  @active.GET
  def _getActiveFlag(self) -> bool:
    """Getter-function for the flag indicating if the push button is
    active."""
    return True if self.__is_enabled__ else False

  def activate(self) -> None:
    """Activates the 'enabled' state of the button"""
    if self.active:
      return
    self.__is_enabled__ = True

  def deactivate(self) -> None:
    """Deactivates the 'enabled' state of the button"""
    if self.active:
      self.__is_enabled__ = False

  @mousePressed.GET
  def _getMousePressedFlag(self) -> bool:
    """Getter-function for the flag indicating if the mouse is pressed
    over the push button."""
    return True if self.__mouse_pressed__ else False

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Stored events

  @pressEvent.GET
  def _getPressEvent(self) -> QPointerEvent:
    """Getter-function for stored press event"""
    return self.__press_event__

  @pressEvent.SET
  def _setPressEvent(self, pointerEvent: QPointerEvent) -> None:
    """Setter-function for stored press event"""
    self.__press_event__ = pointerEvent

  @holdEvent.GET
  def _getHoldEvent(self) -> QPointerEvent:
    """Getter-function for stored hold event"""
    return self.__hold_event__

  @holdEvent.SET
  def _setHoldEvent(self, pointerEvent: QPointerEvent) -> None:
    """Setter-function for stored hold event"""
    self.__hold_event__ = pointerEvent

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Point event handlers

  def handlePointerEvent(self, pointerEvent: QPointerEvent) -> bool:
    """Method handling pointer events"""
    eventPoint = pointerEvent.point(0)
    point = eventPoint.scenePosition() - self.parentRect.topLeft()
    self.__cursor_position__ = point
    eType = pointerEvent.type()
    if eType is QEvent.Type.MouseMove:
      return self.handleMouseMove(pointerEvent)
    if eType is QEvent.Type.MouseButtonPress:
      return self.handleMousePress(pointerEvent)
    if eType is QEvent.Type.MouseButtonDblClick:
      return self.handleMousePress(pointerEvent)
    if eType is QEvent.Type.MouseButtonRelease:
      return self.handleMouseRelease(pointerEvent)
    return False

  def handleMouseMove(self, pointerEvent: QPointerEvent) -> bool:
    """Method handling mouse move events"""
    self.underMouse = True
    self.repaint()
    eventPoint = QPointerEvent.point(pointerEvent, 0)
    v = QEventPoint.velocity(eventPoint)
    self.moveSpeed.emit(QVector2D.length(v))
    self.__mouse_velocity__ = v
    self.__cursor_position__ = QEventPoint.position(eventPoint)
    return True

  def handleMousePress(self, pointerEvent: QPointerEvent) -> bool:
    """Method handling mouse press events"""
    self.__mouse_pressed__ = True
    if QTimer.isActive(self.doubleDelay):
      self.tripleClickTimer.start()
      self.tripleHold.start()
      self.singleDelay.stop()
      self.doubleDelay.stop()
    elif QTimer.isActive(self.singleDelay):
      self.doubleClickTimer.start()
      self.doubleHold.start()
      self.singleDelay.stop()
    else:
      self.singleClickTimer.start()
      self.singleHold.start()
    self.update()
    return True

  def handleMouseRelease(self, pointerEvent: QPointerEvent) -> bool:
    """Method handling mouse release events"""
    self.__mouse_pressed__ = False
    self.mouseRelease.emit()
    self.singleHold.stop()
    self.doubleHold.stop()
    self.tripleHold.stop()
    if QTimer.isActive(self.tripleClickTimer):
      if isinstance(pointerEvent, QMouseEvent):
        self.tripleClick.emit(self.pressEvent)
        self.tripleClickTimer.stop()
        self.doubleClickTimer.stop()
        self.singleClickTimer.stop()
        self.update()
        return True
      return False
    if QTimer.isActive(self.doubleClickTimer):
      self.doubleDelay.start()
      self.singleClickTimer.stop()
      self.update()
      return True
    if QTimer.isActive(self.singleClickTimer):
      self.singleDelay.start()
      self.singleClickTimer.stop()
      self.update()
      return True
    self.update()
    return True

  def handleLeaveEvent(self, pointerEvent: QPointerEvent) -> bool:
    """Method handling leave events"""
    self.mouseLeave.emit()
    self.update()
    return True

  def handleEnterEvent(self, pointerEvent: QPointerEvent) -> bool:
    """Method handling enter events"""
    self.mouseEnter.emit()
    self.update()
    return True

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Signal slot connections

  def initSignalSlot(self) -> None:
    """Initiates the signal slot connections"""
    self.singleHold.timeout.connect(self.singleHoldFunc)
    self.doubleHold.timeout.connect(self.doubleHoldFunc)
    self.tripleHold.timeout.connect(self.tripleHoldFunc)
    self.doubleDelay.timeout.connect(self.doubleClickFunc)
    self.singleDelay.timeout.connect(self.singleClickFunc)

  @Slot()
  def singleHoldFunc(self) -> None:
    """Single press hold limit"""
    self.singleHold.emit(self.holdEvent)

  @Slot()
  def doubleHoldFunc(self) -> None:
    """Double press hold limit"""
    self.doubleHold.emit(self.holdEvent)

  @Slot()
  def tripleHoldFunc(self) -> None:
    """Triple press hold limit"""
    self.tripleHold.emit(self.holdEvent)

  @Slot()
  def doubleClickFunc(self) -> None:
    """Double click release deal"""
    self.doubleClick.emit(self.pressEvent)

  @Slot()
  def singleClickFunc(self) -> None:
    """Single click release """
    self.singleClick.emit(self.pressEvent)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Constructor

  def __init__(self, *args) -> None:
    LayoutWidget.__init__(self, *args)
    self.setMouseTracking(True)
    self.singleClickTimer = MouseTimer(self, ControlData.singleClick)
    self.singleHold = MouseTimer(self, ControlData.singleHold)
    self.singleDelay = MouseTimer(self, ControlData.singleDelay)
    self.doubleClickTimer = MouseTimer(self, ControlData.doubleClick)
    self.doubleHold = MouseTimer(self, ControlData.doubleHold)
    self.doubleDelay = MouseTimer(self, ControlData.doubleDelay)
    self.tripleClickTimer = MouseTimer(self, ControlData.tripleClick)
    self.tripleHold = MouseTimer(self, ControlData.tripleHold)
    self.tripleDelay = MouseTimer(self, ControlData.tripleDelay)
    self.restDelay = MouseTimer(self, ControlData.restDelay)
    self.initSignalSlot()
    self.activate()

  @abstractmethod
  def requiredSize(self) -> QSizeF:
    """This method informs the parent layout of the size this widget at
    minimum requires to render. """

  @abstractmethod
  def getMouseRegion(self) -> QRectF:
    """This method returns the region of this widget that is sensitive to
    pointer events. """

  @abstractmethod
  def getAlignment(self) -> Align:
    """Getter-function for the alignment setting"""
