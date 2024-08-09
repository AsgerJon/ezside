"""PushButton implementation for the ezside library."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QRectF, QPoint, Qt, Signal, QPointF
from PySide6.QtGui import QPainter, QEnterEvent, QMouseEvent
from icecream import ic
from worktoy.desc import Field
from worktoy.text import typeMsg

from ezside.tools import emptyPen
from ezside.basewidgets import Label, ButtonStyle, ButtonState

ic.configureOutput(includeContext=True)


class PushButton(Label):
  """This class provides the state awareness of a push button. """

  __style_data__ = None

  __is_active__ = True
  __under_mouse__ = None
  __mouse_pressed__ = None
  __cursor_position__ = None
  __mouse_region__ = None

  active = Field()
  underMouse = Field()
  mousePressed = Field()
  buttonState = Field()

  x = Field()  # int
  y = Field()  # int
  p = Field()  # QPoint
  cursorPosition = Field()
  mouseRegion = Field()

  state = Field()
  style = Field()
  styleData = Field()

  mouseLeave = Signal()
  mouseEnter = Signal()
  mousePress = Signal()
  mouseRelease = Signal()
  leftClick = Signal()
  rightClick = Signal()
  singleClick = Signal(Qt.MouseButton)
  doubleClick = Signal(Qt.MouseButton)
  tripleClick = Signal(Qt.MouseButton)
  pressHold = Signal(Qt.MouseButton)
  speedClick = Signal(QPointF)

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

  @x.GET
  def _getX(self) -> float:
    """Getter-function for the x-coordinate."""
    return float(self.__cursor_position__.x())

  @y.GET
  def _getY(self) -> float:
    """Getter-function for the y-coordinate."""
    return float(self.__cursor_position__.y())

  @mouseRegion.GET
  def _getMouseRegion(self) -> QRectF:
    """Getter-function for the mouse region."""
    return self.__mouse_region__

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

  @active.GET
  def _getActiveFlag(self) -> bool:
    """Getter-function for the flag indicating if the push button is
    active."""
    return True if self.__is_active__ else False

  @underMouse.GET
  def _getUnderMouseFlag(self) -> bool:
    """Getter-function for the flag indicating if the mouse is over the
    push button."""
    return True if self.__under_mouse__ else False

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

  def paintMeLike(self, rect: QRectF, painter: QPainter) -> None:
    """Paints the push button."""
    viewRect = rect
    center = viewRect.center()
    marginRect = QRectF.marginsRemoved(viewRect, self.style.margins)
    borderRect = QRectF.marginsRemoved(marginRect, self.style.borders)
    paddedRect = QRectF.marginsRemoved(borderRect, self.style.paddings)
    marginRect.moveCenter(center)
    borderRect.moveCenter(center)
    paddedRect.moveCenter(center)
    self.__mouse_region__ = paddedRect
    painter.setPen(emptyPen())
    painter.setBrush(self.style.borderBrush)
    painter.drawRect(marginRect)
    painter.setBrush(self.style.backgroundBrush)
    painter.drawRect(borderRect)
    painter.setPen(self.textFont.asQPen)
    painter.setFont(self.textFont.asQFont)
    textRect = self.textFont.align.fitRectF(self.requiredRect(), paddedRect)
    painter.drawText(textRect, self.textFont.align.qt, self.text)

  def __init__(self, *args) -> None:
    """Initializes the push button."""
    Label.__init__(self, *args)
    self.setMouseTracking(True)

  def enterEvent(self, event: QEnterEvent) -> None:
    """Event handler for when the mouse enters the widget."""
    Label.enterEvent(self, event)
    self.__under_mouse__ = True
    self.__cursor_position__ = event.pos()
    self.mouseEnter.emit()
    self.update()

  def leaveEvent(self, event: QEnterEvent) -> None:
    """Event handler for when the mouse leaves the widget."""
    Label.leaveEvent(self, event)
    self.__under_mouse__ = False
    self.__mouse_pressed__ = False
    self.__cursor_position__ = QPoint(-1, -1)
    self.mouseLeave.emit()
    self.update()

  def mouseMoveEvent(self, event: QMouseEvent) -> None:
    """Event handler for when the mouse moves over the widget."""
    Label.mouseMoveEvent(self, event)
    self.__under_mouse__ = True
    self.__cursor_position__ = event.pos()
    self.update()

  def mousePressEvent(self, event: QMouseEvent) -> None:
    """Event handler for when the mouse is pressed over the widget."""
    Label.mousePressEvent(self, event)
    self.__mouse_pressed__ = True
    if self.underMouse:
      self.mousePress.emit()
    self.update()

  def mouseReleaseEvent(self, event: QMouseEvent) -> None:
    """Event handler for when the mouse is released over the widget."""
    Label.mouseReleaseEvent(self, event)
    self.__mouse_pressed__ = False
    if self.underMouse:
      self.mouseRelease.emit()
      if event.button() == Qt.MouseButton.RightButton:
        self.rightClick.emit()
      if event.button() == Qt.MouseButton.LeftButton:
        self.leftClick.emit()
    self.update()
