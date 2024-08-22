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

from ezside.base_widgets import LayoutWidget
from ezside.style import ButtonState, MouseTimer, Align

ic.configureOutput(includeContext=True)

Rect: TypeAlias = Union[QRect, QRectF]


class AbstractButton(LayoutWidget):
  """BaseButton provides button widgets with mouse awareness. """

  #  Timer settings from JSON
  __control_data__ = None
  __single_click_interval__ = None
  __double_click_interval__ = None
  __triple_click_interval__ = None
  __single_delay_interval__ = None
  __double_delay_interval__ = None
  __triple_delay_interval__ = None
  __single_hold_interval__ = None
  __double_hold_interval__ = None
  __triple_hold_interval__ = None
  #  Timer objects
  __single_click_timer__ = None
  __double_click_timer__ = None
  __triple_click_timer__ = None
  __single_delay_timer__ = None
  __double_delay_timer__ = None
  __triple_delay_timer__ = None
  __single_hold_timer__ = None
  __double_hold_timer__ = None
  __triple_hold_timer__ = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Cursor movement
  __cursor_position__ = None
  __mouse_velocity__ = None
  #  Mouse state-flags
  __is_enabled__ = True
  __mouse_pressed__ = None
  __press_event__ = None
  __hold_event__ = None
  #  Mouse-limit values
  __click_drift__ = None
  __multi_drift__ = None
  __rest_speed__ = None
  __rest_radius__ = None
  __rest_delay__ = None
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Descriptor fields
  singleClickTimer = Field()
  singleHoldTimer = Field()
  singleDelayTimer = Field()
  doubleClickTimer = Field()
  doubleHoldTimer = Field()
  doubleDelayTimer = Field()
  tripleClickTimer = Field()
  tripleHoldTimer = Field()
  tripleDelayTimer = Field()
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

  #  Static methods
  @staticmethod
  def _squareDistance(p0: QPointF, p1: QPointF) -> float:
    """Calculates the distance between two points"""
    return (p0.x() - p1.x()) ** 2 + (p0.y() - p1.y()) ** 2

  #  Timer Functions
  def _createSingleClickTimer(self) -> None:
    """Creates the single click timer"""
    interval = self.controlData.singleClick
    self.__single_click_timer__ = MouseTimer(self, interval)

  @singleClickTimer.GET
  def _getSingleClickTimer(self, **kwargs) -> MouseTimer:
    """Getter-function for the single click timer"""
    if self.__single_click_timer__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createSingleClickTimer()
      return self._getSingleClickTimer(_recursion=True)
    if isinstance(self.__single_click_timer__, MouseTimer):
      return self.__single_click_timer__
    e = typeMsg('singleClickTimer', self.__single_click_timer__, MouseTimer)
    raise TypeError(e)

  def _createSingleHoldTimer(self) -> None:
    """Creates the single hold timer"""
    interval = self.controlData.singleHold
    self.__single_hold_timer__ = MouseTimer(self, interval)

  @singleHoldTimer.GET
  def _getSingleHoldTimer(self, **kwargs) -> MouseTimer:
    """Getter-function for the single hold timer"""
    if self.__single_hold_timer__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createSingleHoldTimer()
      return self._getSingleHoldTimer(_recursion=True)
    if isinstance(self.__single_hold_timer__, MouseTimer):
      return self.__single_hold_timer__
    e = typeMsg('singleHoldTimer', self.__single_hold_timer__, MouseTimer)
    raise TypeError(e)

  def _createSingleDelayTimer(self) -> None:
    """Creates the single delay timer"""
    interval = self.controlData.singleDelay
    self.__single_delay_timer__ = MouseTimer(self, interval)

  @singleDelayTimer.GET
  def _getSingleDelayTimer(self, **kwargs) -> MouseTimer:
    """Getter-function for the single delay timer"""
    if self.__single_delay_timer__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createSingleDelayTimer()
      return self._getSingleDelayTimer(_recursion=True)
    if isinstance(self.__single_delay_timer__, MouseTimer):
      return self.__single_delay_timer__
    e = typeMsg('singleDelayTimer', self.__single_delay_timer__, MouseTimer)
    raise TypeError(e)

  def _createDoubleClickTimer(self) -> None:
    """Creates the double click timer"""
    interval = self.controlData.doubleClick
    self.__double_click_timer__ = MouseTimer(self, interval)

  @doubleClickTimer.GET
  def _getDoubleClickTimer(self, **kwargs) -> MouseTimer:
    """Getter-function for the double click timer"""
    if self.__double_click_timer__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createDoubleClickTimer()
      return self._getDoubleClickTimer(_recursion=True)
    if isinstance(self.__double_click_timer__, MouseTimer):
      return self.__double_click_timer__
    e = typeMsg('doubleClickTimer', self.__double_click_timer__, MouseTimer)
    raise TypeError(e)

  def _createDoubleHoldTimer(self) -> None:
    """Creates the double hold timer"""
    interval = self.controlData.doubleHold
    self.__double_hold_timer__ = MouseTimer(self, interval)

  @doubleHoldTimer.GET
  def _getDoubleHoldTimer(self, **kwargs) -> MouseTimer:
    """Getter-function for the double hold timer"""
    if self.__double_hold_timer__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createDoubleHoldTimer()
      return self._getDoubleHoldTimer(_recursion=True)
    if isinstance(self.__double_hold_timer__, MouseTimer):
      return self.__double_hold_timer__
    e = typeMsg('doubleHoldTimer', self.__double_hold_timer__, MouseTimer)
    raise TypeError(e)

  def _createDoubleDelayTimer(self) -> None:
    """Creates the double delay timer"""
    interval = self.controlData.doubleDelay
    self.__double_delay_timer__ = MouseTimer(self, interval)

  @doubleDelayTimer.GET
  def _getDoubleDelayTimer(self, **kwargs) -> MouseTimer:
    """Getter-function for the double delay timer"""
    if self.__double_delay_timer__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createDoubleDelayTimer()
      return self._getDoubleDelayTimer(_recursion=True)
    if isinstance(self.__double_delay_timer__, MouseTimer):
      return self.__double_delay_timer__
    e = typeMsg('doubleDelayTimer', self.__double_delay_timer__, MouseTimer)
    raise TypeError(e)

  def _createTripleClickTimer(self) -> None:
    """Creates the triple click timer"""
    interval = self.controlData.tripleClick
    self.__triple_click_timer__ = MouseTimer(self, interval)

  @tripleClickTimer.GET
  def _getTripleClickTimer(self, **kwargs) -> MouseTimer:
    """Getter-function for the triple click timer"""
    if self.__triple_click_timer__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createTripleClickTimer()
      return self._getTripleClickTimer(_recursion=True)
    if isinstance(self.__triple_click_timer__, MouseTimer):
      return self.__triple_click_timer__
    e = typeMsg('tripleClickTimer', self.__triple_click_timer__, MouseTimer)
    raise TypeError(e)

  def _createTripleHoldTimer(self) -> None:
    """Creates the triple hold timer"""
    interval = self.controlData.tripleHold
    self.__triple_hold_timer__ = MouseTimer(self, interval)

  @tripleHoldTimer.GET
  def _getTripleHoldTimer(self, **kwargs) -> MouseTimer:
    """Getter-function for the triple hold timer"""
    if self.__triple_hold_timer__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createTripleHoldTimer()
      return self._getTripleHoldTimer(_recursion=True)
    if isinstance(self.__triple_hold_timer__, MouseTimer):
      return self.__triple_hold_timer__
    e = typeMsg('tripleHoldTimer', self.__triple_hold_timer__, MouseTimer)
    raise TypeError(e)

  def _createTripleDelayTimer(self) -> None:
    """Creates the triple delay timer"""
    interval = self.controlData.tripleDelay
    self.__triple_delay_timer__ = MouseTimer(self, interval)

  @tripleDelayTimer.GET
  def _getTripleDelayTimer(self, **kwargs) -> MouseTimer:
    """Getter-function for the triple delay timer"""
    if self.__triple_delay_timer__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createTripleDelayTimer()
      return self._getTripleDelayTimer(_recursion=True)
    if isinstance(self.__triple_delay_timer__, MouseTimer):
      return self.__triple_delay_timer__
    e = typeMsg('tripleDelayTimer', self.__triple_delay_timer__, MouseTimer)
    raise TypeError(e)

  #  Accessor functions

  @controlData.GET
  def _getControlData(self) -> dict:
    """Getter-function for the control data"""
    return self.__control_data__

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
    self.update()
    eventPoint = QPointerEvent.point(pointerEvent, 0)
    v = QEventPoint.velocity(eventPoint)
    self.moveSpeed.emit(QVector2D.length(v))
    self.__mouse_velocity__ = v
    self.__cursor_position__ = QEventPoint.position(eventPoint)
    if self.doubleDelayTimer:
      p0 = self.__cursor_position__
      p1 = QPointerEvent.point(pointerEvent, 0).pressPosition()
      if QPointF.manhattanLength(p0 - p1) > self.controlData.multiClickDrift:
        self.singleClickTimer.stop()
        self.doubleClickTimer.stop()
        self.tripleClickTimer.stop()
        self.doubleDelayTimer.stop()
        self.tripleDelayTimer.stop()
        self.doubleClick.emit(self.pressEvent)
        self.update()
        return True
    if self.singleDelayTimer:
      p0 = self.__cursor_position__
      p1 = QPointerEvent.point(pointerEvent, 0).pressPosition()
      if QPointF.manhattanLength(p0 - p1) > self.controlData.clickDrift:
        self.singleClickTimer.stop()
        self.doubleClickTimer.stop()
        self.tripleClickTimer.stop()
        self.singleDelayTimer.stop()
        self.doubleDelayTimer.stop()
        self.tripleDelayTimer.stop()
        self.singleClick.emit(self.pressEvent)
        self.update()
        return True
    return True

  def handleMousePress(self, pointerEvent: QPointerEvent) -> bool:
    """Method handling mouse press events"""
    self.__mouse_pressed__ = True
    if isinstance(pointerEvent, QMouseEvent):
      self.pressEvent = QMouseEvent(pointerEvent)
      self.holdEvent = QMouseEvent(pointerEvent)
    if QTimer.isActive(self.doubleDelayTimer):
      self.tripleClickTimer.start()
      self.tripleHoldTimer.start()
      self.singleDelayTimer.stop()
      self.doubleDelayTimer.stop()
    elif QTimer.isActive(self.singleDelayTimer):
      self.doubleClickTimer.start()
      self.doubleHoldTimer.start()
      self.singleDelayTimer.stop()
    else:
      self.singleClickTimer.start()
      self.singleHoldTimer.start()
    self.update()
    return True

  def handleMouseRelease(self, pointerEvent: QPointerEvent) -> bool:
    """Method handling mouse release events"""
    self.__mouse_pressed__ = False
    self.mouseRelease.emit()
    self.singleHoldTimer.stop()
    self.doubleHoldTimer.stop()
    self.tripleHoldTimer.stop()
    if QTimer.isActive(self.tripleClickTimer):
      if isinstance(pointerEvent, QMouseEvent):
        self.tripleClick.emit(self.__press_event__)
        self.tripleClickTimer.stop()
        self.doubleClickTimer.stop()
        self.singleClickTimer.stop()
        self.update()
        return True
      return False
    if QTimer.isActive(self.doubleClickTimer):
      self.doubleDelayTimer.start()
      self.singleClickTimer.stop()
      self.update()
      return True
    if QTimer.isActive(self.singleClickTimer):
      self.singleDelayTimer.start()
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
    self.singleHoldTimer.timeout.connect(self.singleHoldFunc)
    self.doubleHoldTimer.timeout.connect(self.doubleHoldFunc)
    self.tripleHoldTimer.timeout.connect(self.tripleHoldFunc)
    self.doubleDelayTimer.timeout.connect(self.doubleClickFunc)
    self.singleDelayTimer.timeout.connect(self.singleClickFunc)

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

  def __init__(self, *args, **kwargs) -> None:
    LayoutWidget.__init__(self, *args, **kwargs)
    self.setMouseTracking(True)
    self.__control_data__ = self.app.loadControl(self.styleId)

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
