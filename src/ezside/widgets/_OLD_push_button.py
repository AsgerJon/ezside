"""PushButton implementation for the ezside library."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import (Signal, QPoint, QRectF, QPointF, QSize,
                            QMarginsF, \
                            Qt)
from PySide6.QtGui import QEnterEvent, QMouseEvent, QColor, QPaintEvent, \
  QPainter, QShowEvent
from icecream import ic
from worktoy.desc import Field, AttriBox
from worktoy.parse import maybe

from ezside.tools import emptyPen, SizeRule, Align, ColorBox
from ezside.widgets import Label, ButtonState, BoxWidget

ic.configureOutput(includeContext=True)


class PushButton(Label):
  """This class provides the state awareness of a push button. """

  #  PRIVATE  # ----------------
  __is_active__ = True
  __under_mouse__ = None
  __mouse_pressed__ = None
  __cursor_position__ = None
  __mouse_region__ = None
  __first_show__ = True
  #  PUBLIC  # -----------------
  active = Field()
  underMouse = Field()
  mousePressed = Field()
  buttonState = Field()
  #  Cursor position  # --------
  x = Field()  # int
  y = Field()  # int
  p = Field()  # QPoint
  cursorPosition = Field()
  mouseRegion = Field()
  #  Signals  # ----------------
  mouseLeave = Signal()
  mouseEnter = Signal()
  mousePress = Signal()
  mouseRelease = Signal()
  leftClick = Signal()
  rightClick = Signal()
  #  State-Boxes # ------------
  disabledHover = AttriBox[BoxWidget]()
  disabledReleased = AttriBox[BoxWidget]()
  disabledPressed = AttriBox[BoxWidget]()
  enabledHover = AttriBox[BoxWidget]()
  enabledReleased = AttriBox[BoxWidget]()
  enabledPressed = AttriBox[BoxWidget]()

  def __init__(self, *args, ) -> None:
    Label.__init__(self, *args, )
    self.setMouseTracking(True)
    self.paddings = 4, 1
    self.font.size = 18
    self.font.align = Align.CENTER
    self.sizeRule = SizeRule.PREFER

    self.disabledHover.paddings = self.paddings
    self.disabledReleased.paddings = self.paddings
    self.disabledPressed.paddings = self.paddings
    self.enabledHover.paddings = self.paddings
    self.enabledReleased.paddings = self.paddings
    self.enabledPressed.paddings = self.paddings

    self.disabledHover.borders = 1
    self.disabledReleased.borders = 0
    self.disabledPressed.borders = 2
    self.enabledHover.borders = 2
    self.enabledReleased.borders = 1
    self.enabledPressed.borders = 4

    self.disabledHover.margins = 0
    self.disabledReleased.margins = 0
    self.disabledPressed.margins = 0
    self.enabledHover.margins = 0
    self.enabledReleased.margins = 0
    self.enabledPressed.margins = 0

    self.disabledHover.backgroundColor = QColor(255, 255, 255, 255)
    self.disabledReleased.backgroundColor = QColor(255, 255, 255, 255)
    self.disabledPressed.backgroundColor = QColor(255, 255, 255, 255)
    self.enabledHover.backgroundColor = QColor(247, 247, 247, 255)
    self.enabledReleased.backgroundColor = QColor(255, 255, 255, 255)
    self.enabledPressed.backgroundColor = QColor(247, 247, 247, 255)

    self.disabledHover.borderColor = QColor(127, 127, 127, 255)
    self.disabledReleased.borderColor = QColor(255, 255, 255, 255)
    self.disabledPressed.borderColor = QColor(127, 127, 127, 255)
    self.enabledHover.borderColor = QColor(0, 0, 0, 255)
    self.enabledReleased.borderColor = QColor(127, 127, 127, 255)
    self.enabledPressed.borderColor = QColor(0, 0, 0, 255)
    self.backgroundColor = QColor(255, 255, 255, 255)
    self.update()

  backgroundColor = ColorBox(QColor(255, 255, 255, 255))

  @backgroundColor.PRESET
  def _handleBGColor(self, oldVal: QColor, newVal: QColor) -> None:
    if newVal == oldVal:
      return
    self.disabledHover.backgroundColor = newVal
    self.disabledReleased.backgroundColor = newVal
    self.disabledPressed.backgroundColor = newVal
    self.enabledHover.backgroundColor = newVal
    self.enabledReleased.backgroundColor = newVal
    self.enabledPressed.backgroundColor = newVal

  def activate(self) -> None:
    """This method activates the button."""
    self.__is_active__ = True
    self.update()

  def deactivate(self) -> None:
    """This method deactivates the button."""
    self.__is_active__ = False
    self.update()

  @active.GET
  def _getActive(self) -> bool:
    """Getter-function for the is_active attribute."""
    return True if self.__is_active__ else False

  def getStateDict(self) -> dict[ButtonState, BoxWidget]:
    """This method returns a dictionary of the state boxes."""
    return {
        ButtonState.DISABLED_HOVER   : self.disabledHover,
        ButtonState.DISABLED_RELEASED: self.disabledReleased,
        ButtonState.DISABLED_PRESSED : self.disabledPressed,
        ButtonState.ENABLED_HOVER    : self.enabledHover,
        ButtonState.ENABLED_RELEASED : self.enabledReleased,
        ButtonState.ENABLED_PRESSED  : self.enabledPressed,
    }

  def stateBox(self) -> BoxWidget:
    """This method returns the state box of the widget."""
    return self.getStateDict()[self.buttonState]

  def getRadius(self, ) -> tuple[int, int]:
    """Corner radii"""
    radii = {
        ButtonState.DISABLED_HOVER   : (1, 1),
        ButtonState.DISABLED_RELEASED: (1, 1),
        ButtonState.DISABLED_PRESSED : (1, 1),
        ButtonState.ENABLED_HOVER    : (4, 4),
        ButtonState.ENABLED_RELEASED : (1, 1),
        ButtonState.ENABLED_PRESSED  : (9, 9),
    }
    return radii[self.buttonState]

  def paintEvent(self, event: QPaintEvent) -> None:
    """Reimplementation"""
    painter = QPainter()
    painter.begin(self)
    viewRect = painter.viewport()
    contentRect = QRectF(QPointF(0, 0), self.requiredSize())
    contentRect += self.stateBox().paddings
    borderRect = contentRect + self.stateBox().borders
    contentRect.moveCenter(viewRect.center())
    borderRect.moveCenter(viewRect.center())
    painter.setPen(emptyPen())
    painter.setBrush(self.stateBox().borderBrush)
    painter.drawRoundedRect(borderRect, *self.getRadius())
    painter.setBrush(self.stateBox().backgroundBrush)
    painter.drawRoundedRect(contentRect, *self.getRadius())
    self.__mouse_region__ = borderRect
    self.font @ painter
    painter.drawText(contentRect, self.font.align.qt, self.text)
    painter.end()

  def minimumSizeHint(self) -> QSize:
    """This method returns the size hint of the widget."""
    borderLeft, borderTop, borderRight, borderBottom = 0, 0, 0, 0
    marginLeft, marginTop, marginRight, marginBottom = 0, 0, 0, 0
    padLeft, padTop, padRight, padBottom = 0, 0, 0, 0
    for (state, box) in self.getStateDict().items():
      borderLeft = max(borderLeft, box.borders.left())
      borderTop = max(borderTop, box.borders.top())
      borderRight = max(borderRight, box.borders.right())
      borderBottom = max(borderBottom, box.borders.bottom())
      marginLeft = max(marginLeft, box.margins.left())
      marginTop = max(marginTop, box.margins.top())
      marginRight = max(marginRight, box.margins.right())
      marginBottom = max(marginBottom, box.margins.bottom())
      padLeft = max(padLeft, box.paddings.left())
      padTop = max(padTop, box.paddings.top())
      padRight = max(padRight, box.paddings.right())
      padBottom = max(padBottom, box.paddings.bottom())
    rect = QRectF(QPointF(0, 0), self.requiredSize())
    borders = QMarginsF(borderLeft, borderTop, borderRight, borderBottom)
    margins = QMarginsF(marginLeft, marginTop, marginRight, marginBottom)
    paddings = QMarginsF(padLeft, padTop, padRight, padBottom)
    rect += borders
    rect += margins
    rect += paddings
    return QRectF.toRect(rect).size()

  @cursorPosition.GET
  def _getCursorPosition(self) -> QPointF:
    """Getter-function for the cursorPosition attribute."""
    return maybe(self.__cursor_position__, QPointF(0, 0))

  @underMouse.GET
  def _getUnderMouse(self) -> bool:
    """Getter-function for the underMouse attribute."""
    if self.__mouse_region__ is None:
      rect = QRectF(QPointF(0, 0), self.requiredSize())
      width, height = 0.5 * self.width(), 0.5 * self.height()
      rect.moveCenter(QPointF(width, height).toPoint())
      self.__mouse_region__ = rect
    rect = self.__mouse_region__
    return True if rect.contains(self.cursorPosition) else False

  @mouseRegion.GET
  def _getMouseRegion(self, **kwargs) -> QRectF:
    """Getter-function for the mouseRegion attribute."""
    if self.__mouse_region__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      rect = QRectF(QPointF(0, 0), self.requiredSize())
      width, height = 0.5 * self.width(), 0.5 * self.height()
      rect.moveCenter(QPointF(width, height).toPoint())
      self.__mouse_region__ = rect
      return self._getMouseRegion(_recursion=True)
    return self.__mouse_region__

  @mousePressed.GET
  def _getMousePressed(self) -> bool:
    """Getter-function for the mousePressed attribute."""
    return True if self.__mouse_pressed__ else False

  @buttonState.GET
  def _getButtonState(self) -> ButtonState:
    """Getter-function for the button state."""
    if self.active:
      if self.underMouse:
        if self.mousePressed:
          return ButtonState.ENABLED_PRESSED
        return ButtonState.ENABLED_HOVER
      return ButtonState.ENABLED_RELEASED
    if self.underMouse:
      if self.mousePressed:
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

  def showEvent(self, event: QShowEvent) -> None:
    """Event handler for when the widget is shown."""
    if self.__first_show__:
      self.backgroundColor = QColor(255, 255, 255, 255)
      self.__first_show__ = False
    Label.showEvent(self, event)
