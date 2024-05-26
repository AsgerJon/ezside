"""PushButton provides a descriptor class for push buttons. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from random import randint
from typing import TYPE_CHECKING

from PySide6.QtCore import QEvent, QMargins, QPoint
from PySide6.QtGui import QBrush, QColor, QEnterEvent, QPen, QPainter
from PySide6.QtGui import QMouseEvent, QFont
from attribox import AttriBox
from vistutils.fields import EmptyField

from ezside.app import EZDesc
from ezside.desc import AlignCenter, EZTimer, parseBrush, SolidFill, Yellow
from ezside.widgets import CanvasWidget, GraffitiVandal


class PushButtonWidget(CanvasWidget):
  """PushButtonWidget provides a widget class for push buttons. """

  __is_enabled__ = None
  __is_hovered__ = None
  __is_pressed__ = None

  text = AttriBox[str]()
  timer = EZTimer(20)
  __running_time__ = AttriBox[float](0.0)

  down = EmptyField()
  under = EmptyField()
  moving = EmptyField()

  textFont = EmptyField()
  textPen = EmptyField()
  backgroundBrush = EmptyField()
  paddingGeometry = EmptyField()
  borderGeometry = EmptyField()
  marginGeometry = EmptyField()
  cornerRadius = EmptyField()

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the PushButtonWidget."""
    CanvasWidget.__init__(self, *args, **kwargs)
    self.setMouseTracking(True)
    for arg in args:
      if isinstance(arg, str):
        self.text = arg
        break
    self.__is_enabled__ = True

  def enterEvent(self, event: QEnterEvent) -> None:
    """Handles the enter event."""
    self.__is_hovered__ = True
    self.update()
    CanvasWidget.enterEvent(self, event)

  def leaveEvent(self, event: QEvent) -> None:
    """Handles the leave event."""
    self.__is_hovered__ = False
    self.update()
    CanvasWidget.leaveEvent(self, event)

  def mousePressEvent(self, event: QMouseEvent) -> None:
    """Handles the mouse press event."""
    self.__is_pressed__ = True
    self.update()
    CanvasWidget.mousePressEvent(self, event)

  def mouseReleaseEvent(self, event: QMouseEvent) -> None:
    """Handles the mouse release event."""
    self.__is_pressed__ = False
    self.text = 'lmao: %d' % randint(0, 255)
    self.update()
    CanvasWidget.mouseReleaseEvent(self, event)

  def _getMarginBrush(self, ) -> QBrush:
    """Getter-function for border brush"""
    if self.__is_enabled__:
      if self.__is_pressed__:
        return parseBrush(QColor(0, 0, 0, 255), SolidFill)
      if self.__is_hovered__:
        return parseBrush(QColor(239, 239, 239, 255), SolidFill)
      return parseBrush(QColor(239, 239, 239, 255), SolidFill)
    else:
      if self.__is_pressed__:
        return parseBrush(QColor(239, 239, 239, 255), SolidFill)
      if self.__is_hovered__:
        return parseBrush(QColor(239, 239, 239, 255), SolidFill)
      return parseBrush(QColor(239, 239, 239, 255), SolidFill)

  def _getBorderBrush(self, ) -> QBrush:
    """Getter-function for border brush"""
    return parseBrush(Yellow, SolidFill)

  def _getPaddingBrush(self, ) -> QBrush:
    """Getter-function for padding brush"""
    if self.__is_enabled__:
      if self.__is_pressed__:
        return parseBrush(QColor(0, 0, 0, 255), SolidFill)
      if self.__is_hovered__:
        return parseBrush(QColor(239, 239, 239, 255), SolidFill)
      return parseBrush(QColor(239, 239, 239, 255), SolidFill)
    else:
      if self.__is_pressed__:
        return parseBrush(QColor(239, 239, 239, 255), SolidFill)
      if self.__is_hovered__:
        return parseBrush(QColor(239, 239, 239, 255), SolidFill)
      return parseBrush(QColor(239, 239, 239, 255), SolidFill)

  @cornerRadius.GET
  def _getCornerRadius(self) -> QPoint:
    """Returns the corner radius."""
    if self.__is_enabled__:
      if self.__is_pressed__:
        return self.app.pressedEnabledCornerRadius
      if self.__is_hovered__:
        return self.app.hoveredEnabledCornerRadius
      return self.app.defaultEnabledCornerRadius
    else:
      if self.__is_pressed__:
        return self.app.pressedDisabledCornerRadius
      if self.__is_hovered__:
        return self.app.hoveredDisabledCornerRadius
      return self.app.defaultDisabledCornerRadius

  @textFont.GET
  def _getTextFont(self) -> QFont:
    """Returns the text font."""
    if self.__is_enabled__:
      if self.__is_pressed__:
        return self.app.pressedEnabledTextFont
      if self.__is_hovered__:
        return self.app.hoveredEnabledTextFont
      return self.app.defaultEnabledTextFont
    else:
      if self.__is_pressed__:
        return self.app.pressedDisabledTextFont
      if self.__is_hovered__:
        return self.app.hoveredDisabledTextFont
      return self.app.defaultDisabledTextFont

  @textPen.GET
  def _getTextPen(self) -> QPen:
    """Returns the text pen."""
    if self.__is_enabled__:
      if self.__is_pressed__:
        return self.app.pressedEnabledTextPen
      if self.__is_hovered__:
        return self.app.hoveredEnabledTextPen
      return self.app.defaultEnabledTextPen
    else:
      if self.__is_pressed__:
        return self.app.pressedDisabledTextPen
      if self.__is_hovered__:
        return self.app.hoveredDisabledTextPen
      return self.app.defaultDisabledTextPen

  @backgroundBrush.GET
  def _getBackgroundBrush(self) -> QBrush:
    """Returns the background brush."""
    if self.__is_enabled__:
      if self.__is_pressed__:
        return self.app.pressedEnabledBackgroundBrush
      if self.__is_hovered__:
        return self.app.hoveredEnabledBackgroundBrush
      return self.app.defaultEnabledBackgroundBrush
    else:
      if self.__is_pressed__:
        return self.app.pressedDisabledBackgroundBrush
      if self.__is_hovered__:
        return self.app.hoveredDisabledBackgroundBrush
      return self.app.defaultDisabledBackgroundBrush

  @paddingGeometry.GET
  def _getPadding(self) -> QMargins:
    """Returns the padding."""
    if self.__is_enabled__:
      if self.__is_pressed__:
        return self.app.pressedEnabledPadding
      if self.__is_hovered__:
        return self.app.hoveredEnabledPadding
      return self.app.defaultEnabledPadding
    else:
      if self.__is_pressed__:
        return self.app.pressedDisabledPadding
      if self.__is_hovered__:
        return self.app.hoveredDisabledPadding
      return self.app.defaultDisabledPadding

  @borderGeometry.GET
  def _getBorders(self) -> QMargins:
    """Returns the borders."""
    if self.__is_enabled__:
      if self.__is_pressed__:
        return self.app.pressedEnabledBorders
      if self.__is_hovered__:
        return self.app.hoveredEnabledBorders
      return self.app.defaultEnabledBorders
    else:
      if self.__is_pressed__:
        return self.app.pressedDisabledBorders
      if self.__is_hovered__:
        return self.app.hoveredDisabledBorders
      return self.app.defaultDisabledBorders

  @marginGeometry.GET
  def _getMargins(self) -> QMargins:
    """Returns the margins."""
    if self.__is_enabled__:
      if self.__is_pressed__:
        return self.app.pressedEnabledMargins
      if self.__is_hovered__:
        return self.app.hoveredEnabledMargins
      return self.app.defaultEnabledMargins
    else:
      if self.__is_pressed__:
        return self.app.pressedDisabledMargins
      if self.__is_hovered__:
        return self.app.hoveredDisabledMargins
      return self.app.defaultDisabledMargins

  def initUi(self, ) -> None:
    """Initializes the user interface."""
    self.setMinimumSize(120, 120)
    self.timer.timeout.connect(self._maybeUpdate)
    self.timer.start()

  def _maybeUpdate(self) -> None:
    """Maybe updates the widget."""
    if self.__is_hovered__:
      self.update()

  def customPaint(self, painter: GraffitiVandal) -> None:
    """Custom paint event."""
    viewRect = painter.viewport()
    if TYPE_CHECKING:
      assert isinstance(self.backgroundBrush, QBrush)
      assert isinstance(self.textPen, QPen)
      assert isinstance(self.marginGeometry, QMargins)
      assert isinstance(self.borderGeometry, QMargins)
      assert isinstance(self.paddingGeometry, QMargins)
      assert isinstance(self.textFont, QFont)
      assert isinstance(self.cornerRadius, QPoint)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
    painter.setBrush(self.backgroundBrush)
    rx, ry = self.cornerRadius.x(), self.cornerRadius.y()
    painter.drawRoundedRect(viewRect, rx, ry)
    painter.setPen(self.textPen)
    painter.setFont(self.textFont)
    textRect = painter.boundingRect(viewRect, self.text)
    textRect.moveCenter(viewRect.center())
    painter.drawText(textRect, AlignCenter, self.text)
    periphery = 2 * (viewRect.width() + viewRect.height())
    self.__running_time__ += 0.25 * self.timer.interval() / 1000
    if self.__running_time__ > 1:
      self.__running_time__ = 0
    t = self.__running_time__ * periphery
    if t < viewRect.width():
      x = t
      y = 0
    elif t < viewRect.width() + viewRect.height():
      x = viewRect.width()
      y = t - viewRect.width()
    elif t < 2 * viewRect.width() + viewRect.height():
      x = 2 * viewRect.width() + viewRect.height() - t
      y = viewRect.height()
    else:
      x = 0
      y = 2 * viewRect.width() + 2 * viewRect.height() - t
    x = max(0, x)
    x = min(viewRect.width() - 16, x)
    y = max(0, y)
    y = min(viewRect.height() - 16, y)
    painter.setBrush(QColor(255, 0, 0))
    painter.drawEllipse(x, y, 16, 16)


class PushButton(EZDesc):
  """PushButton provides a descriptor class for push buttons. """

  def getContentClass(self) -> type:
    """Returns the content class."""
    return PushButtonWidget

  def create(self,
             instance: object,
             owner: type,
             **kwargs) -> PushButtonWidget:
    """Create the content."""
    return PushButtonWidget(*self.getArgs(), **self.getKwargs())
