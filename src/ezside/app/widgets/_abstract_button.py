"""ButtonWidget provides the baseclass for widgets intended for user
inputs at single points. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, Self, Any

from PySide6.QtCore import Qt, QEvent, Signal, QPoint, Slot, QTimer, QSize
from PySide6.QtGui import QMouseEvent, QEnterEvent, QPainter
from worktoy.text import typeMsg
from worktoy.desc import Field, AttriBox

from . import AbstractWidget
from ..core import BoxModel, Margin, Rect, Font, RGBA, TextModel
from ..enums import Align


class AbstractButton(AbstractWidget):
  """ButtonWidget provides the baseclass for widgets intended for user
  inputs at single points."""

  #  Config values
  #  - Click Press Time and Movement
  #    A mouse click happens when the button is released after being
  #    pressed. The release must happen within this time to be considered a
  #    click. If the release happens after this time, no click happens.
  __press_release_time__ = 300  # milliseconds
  __press_release_distance__ = 10  # pixels
  __chain_press_time__ = 150  # milliseconds
  __chain_press_distance__ = 5  # pixels
  __press_hold_time__ = 500  # milliseconds
  __press_hold_distance__ = 4  # pixels
  #  Private variables
  #  - Flags
  __under_mouse__ = None
  __is_enabled__ = True
  __is_pressed__ = None
  #  - Dynamic attributes
  __mouse_move_x__ = None
  __mouse_move_y__ = None
  __mouse_press_x__ = None
  __mouse_press_y__ = None
  __mouse_btn__ = None
  __press_count__ = 0
  #  - Timers
  __press_release_timer__ = None
  __chain_press_timer__ = None
  __press_hold_timer__ = None

  #  Public variables
  #   - Fields
  pressReleaseTimer = Field()
  chainPressTimer = Field()
  pressHoldTimer = Field()
  isEnabled = Field()
  isPressed = Field()
  underMouse = Field()
  movePos = Field()
  pressPos = Field()
  btn = Field()
  shadowColor = AttriBox[RGBA](0, 0, 0, 31)
  shadowMargin = AttriBox[Margin](8, 1, 8, 1)

  #  - Signals
  singleClick = Signal(Qt.MouseButton, QPoint)
  singlePressHold = Signal(Qt.MouseButton, QPoint)
  doubleClick = Signal(Qt.MouseButton, QPoint)
  doublePressHold = Signal(Qt.MouseButton, QPoint)
  tripleClick = Signal(Qt.MouseButton, QPoint)
  triplePressHold = Signal(Qt.MouseButton, QPoint)
  enteredPos = Signal(QPoint)
  leftPos = Signal(QPoint)

  #  - Creator functions
  def _createPressReleaseTimer(self) -> None:
    """Creates the timer for press-release events. """
    if self.__press_release_timer__ is not None:
      e = """Press-release timer already exists."""
      raise ValueError(e)
    self.__press_release_timer__ = QTimer()
    self.__press_release_timer__.setSingleShot(True)
    self.__press_release_timer__.setInterval(self.__press_release_time__)
    self.__press_release_timer__.setTimerType(Qt.TimerType.PreciseTimer)

  def _createChainPressTimer(self) -> None:
    """Creates the timer for chain-press events. """
    if self.__chain_press_timer__ is not None:
      e = """Chain-press timer already exists."""
      raise ValueError(e)
    self.__chain_press_timer__ = QTimer()
    self.__chain_press_timer__.setSingleShot(True)
    self.__chain_press_timer__.setInterval(self.__chain_press_time__)
    self.__chain_press_timer__.setTimerType(Qt.TimerType.PreciseTimer)

  def _createPressHoldTimer(self) -> None:
    """Creates the timer for press-hold events. """
    if self.__press_hold_timer__ is not None:
      e = """Press-hold timer already exists."""
      raise ValueError(e)
    self.__press_hold_timer__ = QTimer()
    self.__press_hold_timer__.setSingleShot(True)
    self.__press_hold_timer__.setInterval(self.__press_hold_time__)
    self.__press_hold_timer__.setTimerType(Qt.TimerType.PreciseTimer)

  #  - Getter-functions
  @pressReleaseTimer.GET
  def _getPressReleaseTimer(self, **kwargs) -> QTimer:
    """Getter-function for the press-release timer. """
    if self.__press_release_timer__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createPressReleaseTimer()
      return self._getPressReleaseTimer(_recursion=True)
    if isinstance(self.__press_release_timer__, QTimer):
      return self.__press_release_timer__
    e = typeMsg(
        '__press_release_timer__',
        self.__press_release_timer__,
        QTimer)
    raise TypeError(e)

  @chainPressTimer.GET
  def _getChainPressTimer(self, **kwargs) -> QTimer:
    """Getter-function for the chain-press timer. """
    if self.__chain_press_timer__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createChainPressTimer()
      return self._getChainPressTimer(_recursion=True)
    if isinstance(self.__chain_press_timer__, QTimer):
      return self.__chain_press_timer__
    e = typeMsg('__chain_press_timer__', self.__chain_press_timer__, QTimer)
    raise TypeError(e)

  @pressHoldTimer.GET
  def _getPressHoldTimer(self, **kwargs) -> QTimer:
    """Getter-function for the press-hold timer. """
    if self.__press_hold_timer__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createPressHoldTimer()
      return self._getPressHoldTimer(_recursion=True)
    if isinstance(self.__press_hold_timer__, QTimer):
      return self.__press_hold_timer__
    e = typeMsg('__press_hold_timer__', self.__press_hold_timer__, QTimer)
    raise TypeError(e)

  @isEnabled.GET
  def _getIsEnabled(self) -> bool:
    """Getter-function for the enabled state. """
    return True if self.__is_enabled__ else False

  @isPressed.GET
  def _getIsPressed(self) -> bool:
    """Getter-function for the pressed state. """
    return True if self.__is_pressed__ else False

  @underMouse.GET
  def _getUnderMouse(self) -> bool:
    """Getter-function for the under-mouse state. """
    return True if self.__under_mouse__ else False

  @movePos.GET
  def _getMovePos(self) -> QPoint:
    """Getter-function for the current mouse position. """
    if self.__mouse_move_x__ is None or self.__mouse_move_y__ is None:
      return QPoint(-1, -1)
    return QPoint(self.__mouse_move_x__, self.__mouse_move_y__)

  @pressPos.GET
  def _getPressPos(self) -> QPoint:
    """Getter-function for the mouse position when pressed. """
    if self.__mouse_press_x__ is None or self.__mouse_press_y__ is None:
      return QPoint(-1, -1)
    return QPoint(self.__mouse_press_x__, self.__mouse_press_y__)

  @btn.GET
  def _getBtn(self) -> Qt.MouseButton:
    """Getter-function for the mouse button. """
    if self.__mouse_btn__ is None:
      return Qt.MouseButton.NoButton
    if isinstance(self.__mouse_btn__, Qt.MouseButton):
      return self.__mouse_btn__
    e = typeMsg('btn', self.__mouse_btn__, Qt.MouseButton)
    raise TypeError(e)

  #  - Shared methods
  def _stopTimers(self) -> None:
    """Stops all timers. """
    if TYPE_CHECKING:
      assert isinstance(self.pressReleaseTimer, QTimer)
      assert isinstance(self.chainPressTimer, QTimer)
      assert isinstance(self.pressHoldTimer, QTimer)
    self.pressReleaseTimer.stop()
    self.chainPressTimer.stop()
    self.pressHoldTimer.stop()

  def _clearButton(self) -> None:
    """Clears information about which button is pressed. """
    self.__mouse_btn__ = None
    self.__press_count__ = 0

  #  - Event-handlers
  def enterEvent(self, event: QEnterEvent) -> None:
    """Event-handler for when the mouse enters the widget. """
    self.__under_mouse__ = True
    self.enteredPos.emit(event.pos())
    AbstractWidget.enterEvent(self, event)
    self.update()

  def leaveEvent(self, event: QEvent) -> None:
    """Event-handler for when the mouse leaves the widget. """
    self.__under_mouse__ = False
    self.leftPos.emit(self.movePos)
    self._stopTimers()
    self.__press_count__ = 0
    AbstractWidget.leaveEvent(self, event)
    self.update()

  def mouseMoveEvent(self, event: QMouseEvent) -> None:
    """Event-handler for when the mouse moves. """
    if TYPE_CHECKING:
      assert isinstance(self.pressReleaseTimer, QTimer)
      assert isinstance(self.chainPressTimer, QTimer)
      assert isinstance(self.pressHoldTimer, QTimer)
    self.__under_mouse__ = True
    if self.__mouse_press_x__ is None or self.__mouse_press_y__ is None:
      dx, dy = 0, 0
    else:
      dx = (event.x() - self.__mouse_press_x__) ** 2
      dy = (event.y() - self.__mouse_press_y__) ** 2
    if self.isPressed:
      if self.pressReleaseTimer.isActive():
        if dx + dy > self.__press_release_distance__ ** 2:
          self.pressReleaseTimer.stop()

      if self.pressHoldTimer.isActive():
        if dx + dy > self.__press_hold_distance__ ** 2:
          self.pressHoldTimer.stop()
    else:
      if self.chainPressTimer.isActive():
        if dx + dy > self.__chain_press_distance__ ** 2:
          self._stopTimers()
          self.__press_count__ = 0
          self.singleClick.emit(self.btn, self.pressPos)
    self.__mouse_move_x__ = event.x()
    self.__mouse_move_y__ = event.y()
    AbstractWidget.mouseMoveEvent(self, event)
    self.update()

  def mousePressEvent(self, event: QMouseEvent) -> None:
    """Event-handler for when the mouse is pressed. """
    if TYPE_CHECKING:
      assert isinstance(self.pressReleaseTimer, QTimer)
      assert isinstance(self.chainPressTimer, QTimer)
      assert isinstance(self.pressHoldTimer, QTimer)
    if self.chainPressTimer.isActive():
      self.chainPressTimer.stop()
      self.__press_count__ += 1
    self.__under_mouse__ = True
    self.__is_pressed__ = True
    self.__mouse_press_x__ = event.x()
    self.__mouse_press_y__ = event.y()
    self.__mouse_btn__ = event.button()
    self.pressReleaseTimer.start()
    self.pressHoldTimer.start()
    self.update()
    AbstractWidget.mousePressEvent(self, event)

  def mouseReleaseEvent(self, event: QMouseEvent) -> None:
    """Event-handler for when the mouse is released. """
    if TYPE_CHECKING:
      assert isinstance(self.pressReleaseTimer, QTimer)
      assert isinstance(self.chainPressTimer, QTimer)
      assert isinstance(self.pressHoldTimer, QTimer)
    self.__under_mouse__ = True
    self.__is_pressed__ = False
    self.__mouse_btn__ = event.button()
    if self.pressHoldTimer.isActive():
      self.pressHoldTimer.stop()
    if self.pressReleaseTimer.isActive():
      self.pressReleaseTimer.stop()
      self.chainPressTimer.start()
    self.update()
    AbstractWidget.mouseReleaseEvent(self, event)

  #  - Timed functions
  def _chainPressTimeout(self) -> None:
    """Timeout function for chain-press events. """
    if not self.__press_count__:
      return self.singleClick.emit(self.btn, self.pressPos)
    if self.__press_count__ == 1:
      self.doubleClick.emit(self.btn, self.pressPos)
    elif self.__press_count__ == 2:
      self.doubleClick.emit(self.btn, self.pressPos)
    elif self.__press_count__ == 3:
      self.tripleClick.emit(self.btn, self.pressPos)
    self.__press_count__ = 0

  def _pressHoldTimeout(self) -> None:
    """Timeout function for press-hold events. """
    if not self.__press_count__:
      return self.singlePressHold.emit(self.btn, self.pressPos)
    if self.__press_count__ == 1:
      self.doublePressHold.emit(self.btn, self.pressPos)
    elif self.__press_count__ == 2:
      self.triplePressHold.emit(self.btn, self.pressPos)

  def initUi(self, ) -> None:
    """Connects internal signals and slots. Subclasses that reimplement
    this method should invoke the parent method. """
    if TYPE_CHECKING:
      assert isinstance(self.pressReleaseTimer, QTimer)
      assert isinstance(self.chainPressTimer, QTimer)
      assert isinstance(self.pressHoldTimer, QTimer)
    self.chainPressTimer.timeout.connect(self._chainPressTimeout)
    self.pressHoldTimer.timeout.connect(self._pressHoldTimeout)
    self.updateGeometry()
