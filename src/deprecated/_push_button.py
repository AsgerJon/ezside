"""PushButton implementation for the ezside library."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TypeAlias, Union, Any, Never

from PySide6.QtCore import QRect, QEvent, QTimer, Slot, QMarginsF, QSizeF
from PySide6.QtGui import (QPaintEvent, QPointerEvent, QVector2D,
                           QEventPoint, \
                           QColor, QBrush)
from PySide6.QtCore import QRectF, QPoint, Qt, Signal, QPointF
from PySide6.QtGui import QPainter, QEnterEvent, QMouseEvent
from icecream import ic
from worktoy.desc import Field, AttriBox
from worktoy.parse import maybe
from worktoy.text import typeMsg, monoSpace

from ezside.tools import emptyPen, fillBrush, FontCap, Font, FontFamily, \
  ButtonState
from ezside.base_widgets import ButtonStyle, ButtonSettings, LayoutWidget

ic.configureOutput(includeContext=True)

Rect: TypeAlias = Union[QRect, QRectF]


class PushButton(LayoutWidget):
  """This class provides the state awareness of a push button. """

  #  Fallback data
  __fallback_text__ = 'LABEL'

  #  Mouse settings data
  __style_data__ = None  # CSS-like settings from JSON
  __control_data__ = None  # Timer settings from JSON
  #  Mouse movement
  __cursor_position__ = None
  __mouse_region__ = None
  __mouse_velocity__ = None
  #  Mouse state-flags
  __is_enabled__ = True
  __mouse_pressed__ = None
  __pressed_button__ = None
  #  Mouse-timers
  __single_click_limit__ = None
  __single_press_hold_limit__ = None
  __single_release_click_delay__ = None
  __double_click_limit__ = None
  __double_press_hold_limit__ = None
  __double_release_click_delay__ = None
  __triple_click_limit__ = None
  __triple_press_hold_limit__ = None
  # AttriBoxes
  textFont = AttriBox[Font](16, FontFamily.MONTSERRAT, FontCap.MIX)
  text = AttriBox[str]()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  State-flags
  active = Field()
  mousePressed = Field()
  #  Button-state
  buttonState = Field()
  pressedButton = Field()
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Cursor-position
  x = Field()  # int
  y = Field()  # int
  p = Field()  # QPoint
  cursorPosition = Field()
  #  Cursor-velocity
  vx = Field()  # float
  vy = Field()  # float
  v = Field()  # QPointF
  cursorVelocity = Field()
  #  Mouse-region
  mouseRegion = Field()
  #  Mouse-timers
  singleClickLimit = Field()  # If held longer, prevents click
  singlePressHoldLimit = Field()  # When held this long, emits pressHold
  singleReleaseClickDelay = Field()  # Delay for dbl click
  doubleClickLimit = Field()  # If held longer, prevents dbl click
  doublePressHoldLimit = Field()  # When held this long, doublePressHold
  doubleReleaseClickDelay = Field()  # Delay for triple click
  tripleClickLimit = Field()  # If held longer, prevents triple click
  triplePressHoldLimit = Field()  # When held this long, triplePressHold
  #  State-sensitive fields
  state = Field()
  style = Field()
  #  Settings
  styleData = Field()
  controlData = Field()

  #  Signals
  mouseLeave = Signal()
  mouseEnter = Signal()
  mousePress = Signal()
  mouseRelease = Signal()
  singleClick = Signal(Qt.MouseButton)
  doubleClick = Signal(Qt.MouseButton)
  tripleClick = Signal(Qt.MouseButton)
  singleHold = Signal(Qt.MouseButton)
  doubleHold = Signal(Qt.MouseButton)
  tripleHold = Signal(Qt.MouseButton)
  speedClick = Signal(QPointF)
  #  Timer signals
  singleClickLimitSignal = Signal()
  singlePressHoldLimitSignal = Signal()
  singleReleaseClickDelaySignal = Signal()
  doubleClickLimitSignal = Signal()
  doublePressHoldLimitSignal = Signal()
  doubleReleaseClickDelaySignal = Signal()
  tripleClickLimitSignal = Signal()
  triplePressHoldLimitSignal = Signal()
  #  Colors
  borderColor = Field()
  backgroundColor = Field()
  margins = Field()
  borders = Field()
  paddings = Field()
  allMargins = Field()
  cornerRadius = Field()
  backgroundBrush = Field()
  borderBrush = Field()

  @vx.GET
  def _getVx(self) -> float:
    """Getter-function for the x-velocity."""
    return float(self.v.x())

  @vy.GET
  def _getVy(self) -> float:
    """Getter-function for the y-velocity."""
    return float(self.v.y())

  @v.GET
  def _getV(self) -> QPointF:
    """Getter-function for the velocity."""
    return QVector2D.toPointF(self.cursorVelocity)

  @cursorVelocity.GET
  def _getCursorVelocity(self) -> QVector2D:
    """Getter-function for the cursor velocity."""
    if self.__mouse_velocity__ is None:
      return QVector2D(QPointF(0, 0))
    if isinstance(self.__mouse_velocity__, QVector2D):
      return self.__mouse_velocity__
    e = typeMsg('cursorVelocity', self.__mouse_velocity__, QVector2D)
    raise TypeError(e)

  @x.GET
  def _getX(self) -> float:
    """Getter-function for the x-coordinate."""
    return float(self.__cursor_position__.x())

  @y.GET
  def _getY(self) -> float:
    """Getter-function for the y-coordinate."""
    return float(self.__cursor_position__.y())

  @p.GET
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

  def _createStyleData(self) -> None:
    """Creates the style data for the push button."""
    self.__style_data__ = {
        ButtonState.DISABLED_HOVER   : ButtonStyle('disabled', 'hover'),
        ButtonState.DISABLED_RELEASED: ButtonStyle('disabled', 'released'),
        ButtonState.DISABLED_PRESSED : ButtonStyle('disabled', 'pressed'),
        ButtonState.ENABLED_HOVER    : ButtonStyle('enabled', 'hover'),
        ButtonState.ENABLED_RELEASED : ButtonStyle('enabled', 'released'),
        ButtonState.ENABLED_PRESSED  : ButtonStyle('enabled', 'pressed'),
    }

  def _createControlData(self, ) -> None:
    """Creates the button settings object"""
    self.__control_data__ = ButtonSettings()

  @controlData.GET
  def _getControlData(self, **kwargs) -> ButtonSettings:
    """Getter-function for control data"""
    if self.__control_data__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createControlData()
      return self._getControlData(_recursion=True)
    if isinstance(self.__control_data__, ButtonSettings):
      return self.__control_data__
    e = typeMsg('controlData', self.__control_data__, ButtonSettings)
    raise TypeError(e)

  @pressedButton.GET
  def _getPressedButton(self) -> Qt.MouseButton:
    """Getter-function for the most recently pressed button"""
    return maybe(self.__pressed_button__, Qt.MouseButton.NoButton)

  @pressedButton.SET
  def _setPressedButton(self, mouseButton: Qt.MouseButton) -> None:
    """Setter-function for the most recently pressed button"""
    self.__pressed_button__ = mouseButton

  @mouseRegion.GET
  def _getMouseRegion(self) -> QRectF:
    """Getter-function for the mouse region."""
    return self.__mouse_region__

  @mouseRegion.SET
  def _setMouseRegion(self, mouseRegion: QRectF) -> None:
    """Setter-function for the mouse region."""
    self.__mouse_region__ = mouseRegion

  @singleClickLimit.GET
  def _getSingleClickLimit(self, **kwargs) -> QTimer:
    """Getter-function for single click limit timer"""
    if self.__single_click_limit__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      timer = QTimer()
      timer.setInterval(self.controlData['singleClickLimit'])
      timer.setTimerType(Qt.TimerType.PreciseTimer)
      timer.setSingleShot(True)
      self.__single_click_limit__ = timer
      return self._getSingleClickLimit(_recursion=True)
    if isinstance(self.__single_click_limit__, QTimer):
      return self.__single_click_limit__
    e = typeMsg('singleClickLimit', self.__single_click_limit__, QTimer)
    raise TypeError(e)

  @singlePressHoldLimit.GET
  def _getSinglePressHoldLimit(self, **kwargs) -> QTimer:
    """Getter-function for single press hold limit"""
    if self.__single_press_hold_limit__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      timer = QTimer()
      timer.setInterval(self.controlData['singlePressHoldLimit'])
      timer.setTimerType(Qt.TimerType.PreciseTimer)
      timer.setSingleShot(True)
      self.__single_press_hold_limit__ = timer
      return self._getSinglePressHoldLimit(_recursion=True)
    if isinstance(self.__single_press_hold_limit__, QTimer):
      return self.__single_press_hold_limit__
    e = typeMsg('__single_press_hold_limit__',
                self.__single_press_hold_limit__,
                QTimer)
    raise TypeError(e)

  @singleReleaseClickDelay.GET
  def _getSingleReleaseClickDelay(self, **kwargs) -> QTimer:
    if self.__single_release_click_delay__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      timer = QTimer()
      timer.setInterval(self.controlData['singleReleaseClickDelay'])
      timer.setTimerType(Qt.TimerType.PreciseTimer)
      timer.setSingleShot(True)
      self.__single_release_click_delay__ = timer
      return self._getSingleReleaseClickDelay(_recursion=True)
    if isinstance(self.__single_release_click_delay__, QTimer):
      return self.__single_release_click_delay__
    e = typeMsg('singleReleaseClickDelay',
                self.__single_release_click_delay__,
                QTimer)
    raise TypeError(e)

  @doubleClickLimit.GET
  def _getDoubleClickLimit(self, **kwargs) -> QTimer:
    """Getter-function for double click limit"""
    if self.__double_click_limit__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      timer = QTimer()
      timer.setInterval(self.controlData['doubleClickLimit'])
      timer.setTimerType(Qt.TimerType.PreciseTimer)
      timer.setSingleShot(True)
      self.__double_click_limit__ = timer
      return self._getDoubleClickLimit(_recursion=True)
    if isinstance(self.__double_click_limit__, QTimer):
      return self.__double_click_limit__
    e = typeMsg('doubleClickLimit',
                self.__double_click_limit__,
                QTimer)
    raise TypeError(e)

  @doublePressHoldLimit.GET
  def _getDoublePressHoldLimit(self, **kwargs) -> QTimer:
    """Getter-function for double press hold limit"""
    if self.__double_press_hold_limit__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      timer = QTimer()
      ic(self.controlData['doublePressHoldLimit'])
      timer.setInterval(self.controlData['doublePressHoldLimit'])
      timer.setTimerType(Qt.TimerType.PreciseTimer)
      timer.setSingleShot(True)
      self.__double_press_hold_limit__ = timer
      return self._getDoublePressHoldLimit(_recursion=True)
    if isinstance(self.__double_press_hold_limit__, QTimer):
      return self.__double_press_hold_limit__
    e = typeMsg('doublePressHoldLimit',
                self.__double_press_hold_limit__,
                QTimer)
    raise TypeError(e)

  @doubleReleaseClickDelay.GET
  def _getDoubleReleaseClick(self, **kwargs) -> QTimer:
    """Getter-function for double release click delay"""
    if self.__double_release_click_delay__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      timer = QTimer()
      timer.setInterval(self.controlData['doubleReleaseClickDelay'])
      timer.setTimerType(Qt.TimerType.PreciseTimer)
      timer.setSingleShot(True)
      self.__double_release_click_delay__ = timer
      return self._getDoubleReleaseClick(_recursion=True)
    if isinstance(self.__double_release_click_delay__, QTimer):
      return self.__double_release_click_delay__
    e = typeMsg('doubleReleaseClickDelay',
                self.__double_release_click_delay__,
                QTimer)
    raise TypeError(e)

  @tripleClickLimit.GET
  def _getTripleClickLimit(self, **kwargs) -> QTimer:
    """Getter-function for triple click limit"""
    if self.__triple_click_limit__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      timer = QTimer()
      timer.setInterval(self.controlData['tripleClickLimit'])
      timer.setTimerType(Qt.TimerType.PreciseTimer)
      timer.setSingleShot(True)
      self.__triple_click_limit__ = timer
      return self._getTripleClickLimit(_recursion=True)
    if isinstance(self.__triple_click_limit__, QTimer):
      return self.__triple_click_limit__
    e = typeMsg('tripleClickLimit',
                self.__triple_click_limit__,
                QTimer)
    raise TypeError(e)

  @triplePressHoldLimit.GET
  def _getTriplePressHoldLimit(self, **kwargs) -> QTimer:
    """Getter-function for triple press hold limit"""
    if self.__triple_press_hold_limit__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      timer = QTimer()
      timer.setInterval(self.controlData['triplePressHoldLimit'])
      timer.setTimerType(Qt.TimerType.PreciseTimer)
      timer.setSingleShot(True)
      self.__triple_press_hold_limit__ = timer
      return self._getTriplePressHoldLimit(_recursion=True)
    if isinstance(self.__triple_press_hold_limit__, QTimer):
      return self.__triple_press_hold_limit__
    e = typeMsg('triplePressHoldLimit',
                self.__triple_press_hold_limit__,
                QTimer)
    raise TypeError(e)

  @borderBrush.GET
  def _getBorderBrush(self) -> QBrush:
    """Getter-function for the borderBrush."""
    return fillBrush(self.borderColor, )

  @backgroundBrush.GET
  def _getBackgroundBrush(self) -> QBrush:
    """Getter-function for the backgroundBrush."""
    return fillBrush(self.backgroundColor, )

  @borderColor.GET
  def _getBorderColor(self) -> QColor:
    """Getter-function for border color. This is taken from the style
    settings. """
    return self.style.borderColor

  @backgroundColor.GET
  def _getBackgroundColor(self) -> QColor:
    """Getter-function for background color. """
    return self.style.backgroundColor

  @margins.GET
  def _getMargins(self) -> QMarginsF:
    """Getter-function for margins"""
    return self.style.margins

  @paddings.GET
  def _getPaddings(self) -> QMarginsF:
    """Getter-function for paddings"""
    return self.style.paddings

  @borders.GET
  def _getBorders(self) -> QMarginsF:
    """Getter-function for borders"""
    return self.style.borders

  @allMargins.GET
  def _getAllMargins(self) -> QMarginsF:
    """Getter-function for sum of margins, paddings and borders"""
    return self.margins + self.borders + self.paddings

  @cornerRadius.GET
  def _getCornerRadius(self) -> QPointF:
    """Getter-function for corner radius"""
    return self.style.cornerRadius

  @backgroundColor.SET
  @borderColor.SET
  @margins.SET
  @borders.SET
  @paddings.SET
  def _ignoreSetters(self) -> Never:
    """Disabled setters"""
    e = """Buttons use the ButtonStyle to provide state aware styles, 
    but receives explicit setter calls to style object!"""
    raise TypeError(monoSpace(e))

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

  @styleData.GET
  def _getStyleData(self, **kwargs) -> dict:
    """Returns the style data for the push button."""
    if self.__style_data__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createStyleData()
      return self._getStyleData(_recursion=True)
    return self.__style_data__

  @state.GET
  def _getState(self) -> ButtonState:
    """Returns the state of the push button."""
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

  @style.GET
  def _getStyle(self) -> dict:
    """Returns the style for the push button."""
    return self.styleData[self.state]

  def paintMeLike(self,
                  rect: Rect,
                  painter: QPainter,
                  event: QPaintEvent) -> Any:
    """Paints the push button."""
    viewRect = rect if isinstance(rect, QRectF) else QRect.toRectF(rect)
    center = viewRect.center()
    marginRect = QRectF.marginsRemoved(viewRect, self.margins)
    borderRect = QRectF.marginsRemoved(marginRect, self.borders)
    paddedRect = QRectF.marginsRemoved(borderRect, self.paddings)
    marginRect.moveCenter(center)
    borderRect.moveCenter(center)
    paddedRect.moveCenter(center)

    rx, ry = self.cornerRadius.x(), self.cornerRadius.y()
    painter.setPen(emptyPen())
    painter.setBrush(self.borderBrush)
    painter.drawRoundedRect(marginRect, rx, ry)
    painter.setBrush(self.backgroundBrush)
    painter.drawRoundedRect(borderRect, rx, ry)
    textRect = self.textFont.boundRect(self.text)
    targetRect = paddedRect - self.allMargins
    alignRect = self.textFont.align.fitRectF(textRect, targetRect)
    painter.setFont(self.textFont.asQFont)
    painter.setPen(self.textFont.asQPen)
    painter.drawText(alignRect, self.textFont.align.qt, self.text)
    return paddedRect, painter, event

  def handlePointerEvent(self, pointerEvent: QPointerEvent) -> bool:
    """Reimplementation to handle pointer events. """
    self.repaint()
    if pointerEvent.pointCount() - 1:
      return False
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

  def handleMouseRelease(self, pointerEvent: QPointerEvent) -> bool:
    """Handles the mouse release event."""
    self.__mouse_pressed__ = False
    self.mouseRelease.emit()
    self.singlePressHoldLimit.stop()
    self.doublePressHoldLimit.stop()
    self.triplePressHoldLimit.stop()
    if QTimer.isActive(self.tripleClickLimit):
      if isinstance(pointerEvent, QMouseEvent):
        self.tripleClick.emit(self.pressedButton)
        self.update()
        return True
      return False
    if QTimer.isActive(self.doubleClickLimit):
      self.doubleReleaseClickDelay.start()
      self.update()
      return True
    if QTimer.isActive(self.singleClickLimit):
      self.singleReleaseClickDelay.start()
      self.update()
      return True
    self.update()
    return True

  def handleMousePress(self, pointerEvent: QPointerEvent) -> bool:
    """Handles the mouse press event."""
    self.__mouse_pressed__ = True
    if isinstance(pointerEvent, QMouseEvent):
      self.pressedButton = QMouseEvent.buttons(pointerEvent)
    if QTimer.isActive(self.doubleReleaseClickDelay):
      self.tripleClickLimit.start()
      self.triplePressHoldLimit.start()
      self.singleReleaseClickDelay.stop()
      self.doubleReleaseClickDelay.stop()
    elif QTimer.isActive(self.singleReleaseClickDelay):
      self.doubleClickLimit.start()
      self.doublePressHoldLimit.start()
      self.singleReleaseClickDelay.stop()
    else:
      self.singleClickLimit.start()
      self.singlePressHoldLimit.start()
    self.update()
    return True

  def handleMouseMove(self, pointerEvent: QPointerEvent) -> bool:
    """Handles the mouse move event."""
    self.underMouse = True
    self.repaint()
    eventPoint = QPointerEvent.point(pointerEvent, 0)
    self.__mouse_velocity__ = QEventPoint.velocity(eventPoint)
    self.__cursor_position__ = QEventPoint.position(eventPoint)
    return True

  def handleEnterEvent(self, pointerEvent: QPointerEvent) -> bool:
    """Handles the mouse enter event."""
    self.mouseEnter.emit()
    self.update()
    return True

  def handleLeaveEvent(self, pointerEvent: QPointerEvent) -> bool:
    """Handles the mouse leave event."""
    self.mouseLeave.emit()
    self.update()
    return True

  def initSignalSlot(self) -> None:
    """Initiates the signal slot connections"""
    self.singlePressHoldLimit.timeout.connect(
        self.singlePressHoldLimitFunc)
    self.doublePressHoldLimit.timeout.connect(
        self.doublePressHoldLimitFunc)
    self.triplePressHoldLimit.timeout.connect(
        self.triplePressHoldTLimitFunc)
    self.doubleReleaseClickDelay.timeout.connect(
        self.doubleReleaseClickDelayFunc)
    self.singleReleaseClickDelay.timeout.connect(
        self.singleReleaseClickDelayFunc)

  @Slot()
  def singlePressHoldLimitFunc(self) -> None:
    """Single press hold limit"""
    self.singleHold.emit(self.pressedButton)

  @Slot()
  def doublePressHoldLimitFunc(self) -> None:
    """Double press hold limit"""
    self.doubleHold.emit(self.pressedButton)

  @Slot()
  def triplePressHoldTLimitFunc(self) -> None:
    """Triple press hold limit"""
    self.tripleHold.emit(self.pressedButton)

  @Slot()
  def doubleReleaseClickDelayFunc(self) -> None:
    """Double click release deal"""
    self.doubleClick.emit(self.pressedButton)

  @Slot()
  def singleReleaseClickDelayFunc(self) -> None:
    """Single click release """
    self.singleClick.emit(self.pressedButton)

  def requiredSize(self) -> QSizeF:
    """Returns the size required to display the current text with the
    current font."""
    rect = self.textFont.boundRect(self.text)
    return (rect + self.allMargins).size()

  def __init__(self, *args) -> None:
    unusedArgs = []
    tempArgs = [*args, ]
    while tempArgs:
      arg = tempArgs.pop(0)
      if isinstance(arg, str):
        self.text = arg
        unusedArgs.extend(tempArgs)
        break
    else:
      self.text = self.__fallback_text__
    LayoutWidget.__init__(self, *unusedArgs)
    self.initSignalSlot()
    self.activate()

  def debug(self) -> None:
    """LMAO"""
    ic(self.margins)
    ic(self.borders)
    ic(self.paddings)
    ic(self.borderColor)
    ic(self.borderBrush)
    ic(self.backgroundColor)
    ic(self.backgroundBrush)
