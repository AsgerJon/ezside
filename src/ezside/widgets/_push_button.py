"""PushButton is a subclass of CanvasWidget providing push button
functionality. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from enum import Enum
from typing import Any

from PySide6.QtCore import QEvent, QMargins, Signal, QPointF
from PySide6.QtGui import QMouseEvent, QEnterEvent, QColor, QFontMetrics
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


class PushButton(Label):
  """PushButton is a subclass of CanvasWidget providing push button
  functionality. """

  _moveTimer = EZTimer(100, Precise, singleShot=True)
  _pressHoldTimer = EZTimer(500, Precise, singleShot=True)
  _releaseTimer = EZTimer(125, Precise, singleShot=True)
  _clickTimer = EZTimer(125, Precise, singleShot=True)
  _doubleReleaseTimer = EZTimer(125, Precise, singleShot=True)
  _doubleClickTimer = EZTimer(125, Precise, singleShot=True)

  __is_enabled__ = True
  __is_checked__ = None
  __is_hovered__ = None
  __is_pressed__ = None
  __is_moving__ = None
  __active_button__ = None
  __recent_mouse__ = None
  __recent_vector__ = None

  mouseEnter = Signal(QPointF)
  mouseLeave = Signal(QPointF)
  mouseMove = Signal(CursorVector)
  singleClick = Signal()
  singleButtonClick = Signal(Click)
  doubleClick = Signal()
  doubleButtonClick = Signal(Click)
  pressHoldButton = Signal(Click)

  def setEnabled(self, enabled: bool) -> None:
    """This method sets the enabled state of the button. """
    self.__is_enabled__ = True if enabled else False
    self.update()

  def initUi(self, ) -> None:
    """Initialize the user interface."""
    self.setSizePolicy(Tight, Tight)
    textRect = QFontMetrics(self.getStyle('font')).boundingRect(self.text)
    outerRect = textRect + self.getStyle('paddings')
    outerRect += self.getStyle('borders')
    outerRect += self.getStyle('margins')
    self.setMouseTracking(True)
    self.initSignalSlot()

  def initSignalSlot(self, ) -> None:
    """Initialize the signal slot."""
    self._moveTimer.timeout.connect(self._movingStop)
    self._pressHoldTimer.timeout.connect(self._pressHoldStop)
    self._releaseTimer.timeout.connect(self._releaseStop)
    self._clickTimer.timeout.connect(self._singleClickStop)
    self._doubleReleaseTimer.timeout.connect(self._doubleReleaseStop)
    self._doubleClickTimer.timeout.connect(self._doubleClickStop)

  def _doubleClickStop(self, ) -> None:
    """If two mouse clicks occur within the double click time limit,
    this timer provides a delay allowing further elevation. Moving the
    mouse during this time emits the double click signal immediately."""
    self.doubleButtonClick.emit(self.__active_button__)
    self._resetState()

  def _doubleReleaseStop(self, ) -> None:
    """If a mouse release event has not occurred for the time set in the
    double release timer, this method is called to stop the double
    release state. Please note, that the 'mouseReleaseEvent' is
    responsible for starting and stopping the timer. """
    self.__is_pressed__ = False

  def _singleClickStop(self) -> None:
    """If a mouse button is clicked, this timer provides a delay that
    allows a second click to elevate to a double click. However, moving
    during this time prevents the double click, which then allows the
    single click to be emitted immediately."""
    self.singleButtonClick.emit(self.__active_button__)
    self._resetState()

  def _pressHoldStop(self) -> None:
    """If a mouse button is held down for the duration of the press hold
    timer, it emits the press hold signal. """
    self.pressHoldButton.emit(self.__active_button__)
    self._resetState()

  def _releaseStop(self) -> None:
    """If a mouse release event has not occurred for the time set in the
    release timer, this method is called to stop the pressed state. Please
    note, that the 'mouseReleaseEvent' is responsible for starting and
    stopping the timer. """
    self.__is_pressed__ = False
    self._pressHoldTimer.start()

  def _movingStop(self) -> None:
    """If a mouse move event has not occurred for the time set in the
    moving timer, this method is called to stop the moving state. Please
    note, that the 'mouseMoveEvent' is responsible for starting and
    stopping the timer. """
    self.__is_moving__ = False

  @staticmethod
  def getStyleTypes() -> dict[str, type]:
    """The styleTypes method provides the type expected at each name. """
    LabelStyleTypes = Label.getStyleTypes()
    ButtonStyleTypes = {'driftLimit': int, 'hAlign': AlignFlag}
    return {**LabelStyleTypes, **ButtonStyleTypes}

  @classmethod
  def getFallbackStyles(cls) -> dict[str, Any]:
    """The fallbackStyles method provides the default values for the
    styles."""
    fallbackStyles = {'driftLimit': 4, 'hAlign': AlignHCenter}
    return {**Label.getFallbackStyles(), **fallbackStyles}

  def getState(self, ) -> str:
    """This method returns the current state of the button. """
    staticState = StaticState.NORMAL
    if not self.__is_enabled__:
      staticState = StaticState.DISABLED
    elif self.__is_checked__:
      staticState = StaticState.CHECKED
    dynamicState = DynamicState.NORMAL
    if self.__is_hovered__:
      dynamicState = DynamicState.HOVER
    if self.__is_pressed__:
      dynamicState = DynamicState.PRESSED
    elif self.__is_moving__:
      dynamicState = DynamicState.MOVING
    return '%s-%s' % (staticState, dynamicState)

  def getDefaultStyles(self, ) -> dict[str, Any]:
    """This implementation defines how the button is rendered depending
    on its current state. The BaseWidget class does not provide state
    awareness on the instance level at runtime, so this method returns the
    dictionary that matches the current state. """
    state = self.getState()
    borderBrush = parseBrush(QColor(223, 223, 223, 255), SolidFill)
    normalNormal = '%s-%s' % (StaticState.NORMAL, DynamicState.NORMAL)
    normalHover = '%s-%s' % (StaticState.NORMAL, DynamicState.HOVER)
    normalPressed = '%s-%s' % (StaticState.NORMAL, DynamicState.PRESSED)
    normalMoving = '%s-%s' % (StaticState.NORMAL, DynamicState.MOVING)

    if state == normalNormal:
      return {
        'padding'        : QMargins(2, 2, 2, 2),
        'borders'        : QMargins(2, 2, 2, 2),
        'borderBrush'    : parseBrush(QColor(0, 0, 0, 144), SolidFill),
        'backgroundBrush': parseBrush(QColor(223, 223, 223, 255), SolidFill),
      }
    if state in [normalHover, normalMoving]:
      return {
        'padding'        : QMargins(2, 2, 2, 2),
        'borders'        : QMargins(2, 2, 2, 2, ),
        'borderBrush'    : parseBrush(QColor(0, 0, 0, 191), SolidFill),
        'backgroundBrush': parseBrush(QColor(191, 191, 191, 255), SolidFill),
      }
    if state in [normalPressed, ]:
      return {
        'padding'        : QMargins(2, 4, 2, 0),
        'borders'        : QMargins(2, 0, 2, 4, ),
        'borderBrush'    : parseBrush(QColor(0, 0, 0, 255), SolidFill),
        'backgroundBrush': parseBrush(QColor(169, 169, 169, 255), SolidFill),
      }

  def enterEvent(self, event: QEnterEvent) -> None:
    """This method is called when the mouse enters the button. """
    type_ = QEvent.Type.MouseMove
    lcl = event.position()
    scn = event.scenePosition()
    glb = event.globalPosition()
    btn = event.button()
    btns = event.buttons()
    mds = event.modifiers()
    event = QMouseEvent(type_, lcl, scn, btn, btns, mds)
    self._updateCursor(event)
    self.__is_hovered__ = True
    self.__is_moving__ = True
    self.mouseEnter.emit(lcl)
    self.update()

  def leaveEvent(self, event: QEvent) -> None:
    """This method is called when the mouse leaves the button. """
    self.mouseLeave.emit(self.__recent_mouse__.position())
    self.__is_hovered__ = False
    self.__is_moving__ = False
    self.__is_pressed__ = False
    self._resetState()
    self.update()

  def mousePressEvent(self, event: QMouseEvent) -> None:
    """This method is called when the mouse is pressed on the button. """
    self.__is_moving__ = False
    self.__is_pressed__ = True
    self.__is_hovered__ = True
    self.__active_button__ = event.button()
    if self._clickTimer.isActive():
      self._clickTimer.stop()
      self._doubleReleaseTimer.start()
    self._releaseTimer.stop()
    self._releaseTimer.start()
    self.update()

  def mouseReleaseEvent(self, event: QMouseEvent) -> None:
    """This method is called when the mouse is released on the button. """
    self.__is_pressed__ = False
    self.__is_hovered__ = True
    if event.button() != self.__active_button__:
      return self._resetState()
    if self._doubleReleaseTimer.isActive():
      self._doubleReleaseTimer.stop()
      self._doubleClickTimer.stop()
      self._doubleClickTimer.start()
    elif self._releaseTimer.isActive():
      self._releaseTimer.stop()
      self._clickTimer.stop()
      self._clickTimer.start()
    elif self._pressHoldTimer.isActive():
      self._pressHoldTimer.stop()
    self.update()

  def mouseMoveEvent(self, event: QMouseEvent) -> None:
    """This method is called when the mouse is moved over the button. """
    self._updateCursor(event)

  def _updateCursor(self, event: QMouseEvent) -> None:
    """This method updates the cursor position. """
    if self.__recent_mouse__ is not None:
      event = QMouseEvent(event)
      recent = QMouseEvent(self.__recent_mouse__)
      timer = self._moveTimer
      if isinstance(recent, QMouseEvent):
        self.__recent_vector__ = CursorVector(recent, event, timer)
        self.mouseMove.emit(self.__recent_vector__)
    self.__recent_mouse__ = QMouseEvent(event)

  def _resetState(self, ) -> None:
    """Method should be triggered in case of unexpected behaviour."""
    self._clickTimer.stop()
    self._doubleReleaseTimer.stop()
    self._doubleClickTimer.stop()
    self._releaseTimer.stop()
    self._moveTimer.stop()
    self._pressHoldTimer.stop()
    self.__is_pressed__ = False
    self.__active_button__ = NoClick
    self.update()
