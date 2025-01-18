"""PressHoldButton provides a button whose activation requires a mouse
press held still within a specified tolerance for a specified duration.
The button includes visual indication of progress and status."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import QTimer, Qt, Signal, Slot, QSize, QRect
from PySide6.QtGui import QMouseEvent, QKeyEvent, QPainter, QBrush
from worktoy.desc import Field
from worktoy.parse import maybe
from worktoy.text import typeMsg

from ezside.core import LabelField, Point, Rect, TextModel, RGBA, Size
from ezside.widgets import PushButton, PaintJob


class PressHoldButton(PushButton):
  """PressHoldButton provides a button whose activation requires a mouse
  press held still within a specified tolerance for a specified duration.
  The button includes visual indication of progress and status."""

  __fallback_rate__ = 30
  __fallback_tolerance__ = 5  # allowed movement in pixels
  __fallback_shade__ = RGBA(144, 255, 0, 63)

  #  Private variables
  __current_frame__ = None  # Private variable
  __frame_rate__ = None  # Private variable
  __animation_timer__ = None  # Private variable
  __move_tolerance__ = None  # Private variable
  __start_pos__ = None  # Private variable
  __shade_color__ = None  # Private variable

  #  Public Field objects
  numFrames = Field()  # int
  currentFrame = Field()  # int
  frameRate = Field()  # int
  frameTime = Field()  # int
  animationTimer = Field()  # QTimer
  progress = Field()  # float
  startPosition = Field()  # Point
  movePosition = Field()  # Point
  moveTolerance = Field()  # int
  shadeColor = Field()  # RGBA

  label = LabelField('LMAO')

  firstFrame = Signal()
  nextFrame = Signal()
  lastFrame = Signal()
  accepted = Signal()
  failed = Signal()

  @shadeColor.GET
  def _getShadeColor(self) -> RGBA:
    """Getter-function for the shadeColor property."""
    value = maybe(self.__shade_color__, self.__fallback_shade__)
    if isinstance(value, RGBA):
      return value
    e = typeMsg('shadeColor', value, RGBA)
    raise TypeError(e)

  @shadeColor.SET
  def _setShadeColor(self, value: RGBA) -> None:
    """Setter-function for the shadeColor property."""
    if isinstance(value, RGBA):
      if value != self.__shade_color__:
        self.__shade_color__ = value
    else:
      e = typeMsg('shadeColor', value, RGBA)
      raise TypeError(e)

  @moveTolerance.GET
  def _getMoveTolerance(self) -> int:
    """Getter-function for the moveTolerance property."""
    value = maybe(self.__move_tolerance__, self.__fallback_tolerance__)
    if isinstance(value, int):
      if value >= 0:
        return value
      e = """Received negative move tolerance: %d!"""
      raise ValueError(e % value)
    e = typeMsg('moveTolerance', value, int)
    raise TypeError(e)

  @frameRate.GET
  def _getFrameRate(self) -> int:
    """Getter-function for the frameRate property."""
    value = maybe(self.__frame_rate__, self.__fallback_rate__)
    if isinstance(value, int):
      if value:
        if value > 0:
          return value
        e = """Received negative frame rate: %d!"""
        raise ValueError(e % value)
      e = """Received zero frame rate!"""
      raise ZeroDivisionError(e)
    e = typeMsg('frameRate', value, int)
    raise TypeError(e)

  @frameTime.GET
  def _getFrameTime(self) -> int:
    """Getter-function for the frameTime property."""
    if TYPE_CHECKING:
      assert isinstance(self.frameRate, int)
    base = 1000 // self.frameRate
    remainder = 1000 % self.frameRate
    if not remainder:
      return int(base)
    if 2 * remainder < self.frameRate:
      return int(base)
    return int(base + 1)

  @currentFrame.GET
  def _getCurrentFrame(self) -> int:
    """Getter-function for the currentFrame property."""
    value = maybe(self.__current_frame__, 0)
    if isinstance(value, int):
      if value >= 0:
        return value
      e = """Received negative current frame: %d!"""
      raise ValueError(e % value)
    e = typeMsg('currentFrame', value, int)
    raise TypeError(e)

  @numFrames.GET
  def _getNumFrames(self) -> int:
    """Getter-function for the total number of frames in the animation. """
    return int(round(self.__press_hold_time__ / self.frameTime))

  def _createAnimationTimer(self) -> None:
    """Create the animation timer."""
    if TYPE_CHECKING:
      assert isinstance(self.frameTime, int)
    self.__animation_timer__ = QTimer()
    self.__animation_timer__.setInterval(self.frameTime)
    self.__animation_timer__.setTimerType(Qt.TimerType.PreciseTimer)
    self.__animation_timer__.setSingleShot(True)

  @animationTimer.GET
  def _getAnimationTimer(self, **kwargs) -> QTimer:
    """Getter-function for the animationTimer property."""
    if self.__animation_timer__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createAnimationTimer()
      return self._getAnimationTimer(_recursion=True)
    if isinstance(self.__animation_timer__, QTimer):
      return self.__animation_timer__
    e = typeMsg('__animation_timer__', self.__animation_timer__, QTimer)
    raise TypeError(e)

  @progress.GET
  def _getProgress(self) -> float:
    """Getter-function for the progress property. This value changes
    linearly from 0 to 1 in equal steps indicating the current progress. """
    if TYPE_CHECKING:
      assert isinstance(self.currentFrame, int)
      assert isinstance(self.numFrames, int)
    return self.currentFrame / self.numFrames

  @startPosition.GET
  def _getStartPosition(self) -> Point:
    """Getter-function for the startPosition property."""
    return Point(self.__mouse_press_x__, self.__mouse_press_y__)

  @movePosition.GET
  def _getMovePosition(self) -> Point:
    """Getter-function for the movePosition property."""
    return Point(self.__mouse_move_x__, self.__mouse_move_y__)

  def _startAnimation(self) -> None:
    """Start the animation."""
    if TYPE_CHECKING:
      assert isinstance(self.animationTimer, QTimer)
    self.update()
    self.animationTimer.start()
    self.firstFrame.emit()
    self.__current_frame__ = 0

  def _advanceAnimation(self, ) -> None:
    """Advance the animation by one frame."""
    if TYPE_CHECKING:
      assert isinstance(self.currentFrame, int)
      assert isinstance(self.numFrames, int)
      assert isinstance(self.animationTimer, QTimer)
    if self.__current_frame__ < self.numFrames:
      self.__current_frame__ += 1
      self.nextFrame.emit()
      self.repaint()
      return self.animationTimer.start()
    return self._finishAnimation()

  def _finishAnimation(self) -> None:
    """Finish the animation."""
    if TYPE_CHECKING:
      assert isinstance(self.animationTimer, QTimer)
    self.animationTimer.stop()
    self.repaint()
    self.lastFrame.emit()

  def mouseMoveEvent(self, event: QMouseEvent) -> None:
    """Handle the mouse move event."""
    if TYPE_CHECKING:
      assert isinstance(self.startPosition, Point)
      assert isinstance(self.movePosition, Point)
      assert isinstance(self.moveTolerance, int)
      assert isinstance(self.animationTimer, QTimer)
    PushButton.mouseMoveEvent(self, event)
    if self.isPressed:
      if abs(self.startPosition - self.movePosition) > self.moveTolerance:
        self.failed.emit()
        self.animationTimer.stop()
        self.repaint()

  def keyPressEvent(self, event: QKeyEvent) -> None:
    """Handle the key press event."""
    if TYPE_CHECKING:
      assert isinstance(self.animationTimer, QTimer)
    PushButton.keyPressEvent(self, event)
    if self.isPressed:
      self.failed.emit()
      self.animationTimer.stop()
      self.repaint()

  def initUi(self, ) -> None:
    """Initialize the user interface."""
    if TYPE_CHECKING:
      assert isinstance(self.label, TextModel)
      assert isinstance(self.animationTimer, QTimer)
    PushButton.initUi(self, )
    self.press.connect(self._startAnimation)
    self.animationTimer.timeout.connect(self._advanceAnimation)

  def paintContent(self, rect: Rect, painter: QPainter) -> PaintJob:
    """Paint the content of the widget."""
    if TYPE_CHECKING:
      assert isinstance(self.label, TextModel)
    rect, painter = PushButton.paintContent(self, rect, painter)
    if self.isPressed:
      self.paintProgress(rect, painter)
    return rect, painter

  def paintProgress(self, rect: Rect, painter: QPainter) -> PaintJob:
    """Paint the progress of the button."""
    if TYPE_CHECKING:
      assert isinstance(self.label, TextModel)
      assert isinstance(self.progress, float)
      assert isinstance(self.shadeColor, RGBA)

    viewRect = painter.viewport()
    topLeft = viewRect.topLeft()
    height = viewRect.height()
    width = int(self.progress * viewRect.width())
    size = QSize(width, height)
    progressRect = QRect(topLeft, size)
    brush = QBrush()
    brush.setColor(self.shadeColor.Q)
    brush.setStyle(Qt.BrushStyle.SolidPattern)
    # paintRect.moveCenter(painter.viewport().center())
    painter.setBrush(brush)
    painter.drawRect(progressRect)

    return rect, painter
