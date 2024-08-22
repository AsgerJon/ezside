"""EventLayout subclasses AbstractLayout and passes mouse events to
widgets it organizes. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QRectF, QPointF, QPoint, QRect, QEvent
from PySide6.QtGui import QMouseEvent, QEnterEvent, QEventPoint
from icecream import ic
from worktoy.desc import Field
from worktoy.text import typeMsg

from ezside.layouts import AbstractLayout
from ezside.base_widgets import BoxWidget

ic.configureOutput(includeContext=True)

TypePress = QEvent.Type.MouseButtonPress
TypeRelease = QEvent.Type.MouseButtonRelease
TypeMouseMove = QEvent.Type.MouseMove
TypeEnter = QEvent.Type.Enter
TypeLeave = QEvent.Type.Leave


class EventLayout(AbstractLayout):
  """EventLayout subclasses AbstractLayout and passes mouse events to
  widgets it organizes. """

  __cursor_position__ = None
  __press_position__ = None
  __mouse_region__ = None
  cursorPosition = Field()
  pressPosition = Field()
  mouseRegion = Field()

  @pressPosition.GET
  def _getPressPosition(self) -> QPointF:
    """Getter-function for press position"""
    if self.__press_position__ is None:
      return QPointF(-1, -1)
    if isinstance(self.__press_position__, QPoint):
      return QPoint.toPointF(self.__press_position__)
    if isinstance(self.__press_position__, QPointF):
      return self.__press_position__
    e = typeMsg('pressPosition', self.__press_position__, QPointF)
    raise TypeError(e)

  @pressPosition.SET
  def _setPressPosition(self, pressPosition: QPointF) -> None:
    """Setter-function for press position"""
    if not isinstance(pressPosition, QPointF):
      e = typeMsg('pressPosition', pressPosition, QPointF)
      raise TypeError(e)
    self.__press_position__ = pressPosition

  @cursorPosition.GET
  def _getCursorPosition(self) -> QPointF:
    """Getter-function for the cursor position"""
    if self.__cursor_position__ is None:
      return QPointF(-1, -1)
    if isinstance(self.__cursor_position__, QPoint):
      return QPoint.toPointF(self.__cursor_position__)
    if isinstance(self.__cursor_position__, QPointF):
      return self.__cursor_position__
    e = typeMsg('cursorPosition', self.__cursor_position__, QPointF)
    raise TypeError(e)

  @cursorPosition.SET
  def _setCursorPosition(self, cursorPosition: QPointF) -> None:
    """Setter-function for the cursor position"""
    if not isinstance(cursorPosition, QPointF):
      e = typeMsg('cursorPosition', cursorPosition, QPointF)
      raise TypeError(e)
    self.__cursor_position__ = cursorPosition

  @mouseRegion.GET
  def _getMouseRegion(self) -> QRectF:
    """Getter-function for the mouse region"""
    if self.__mouse_region__ is None:
      return QRectF()
    if isinstance(self.__mouse_region__, QRect):
      return QRect.toRectF(self.__mouse_region__)
    if isinstance(self.__mouse_region__, QRectF):
      return self.__mouse_region__
    e = typeMsg('mouseRegion', self.__mouse_region__, QRectF)
    raise TypeError(e)

  def leaveEvent(self, event: QEvent) -> None:
    """This method handles the leave event."""
    self.__cursor_position__ = QPointF(-1, -1)
    self.update()

  def enterEvent(self, event: QEnterEvent) -> None:
    """This method handles the enter event."""
    self.__cursor_position__ = event.localPos()
    self.update()

  def mouseMoveEvent(self, event: QMouseEvent) -> None:
    """This method handles the mouse move event."""
    point = (event.points() or [None, ]).pop()
    if isinstance(point, QEventPoint):
      self.cursorPosition = QEventPoint.lastPosition(point)
    else:
      self.cursorPosition = QPointF(-1, -1)
    for item in self.getItems():
      rect = self.getRect(item)
      relPos = QPointF(self.cursorPosition - rect.topLeft()).toPoint()
      if rect.contains(self.cursorPosition):
        newEnter = QEnterEvent(relPos, relPos, relPos)
        btn = event.buttons()
        mdf = event.modifiers()
        newMove = QMouseEvent(TypeMouseMove, relPos, btn, btn, mdf)
        if not item.widgetItem.underMouse:
          item.widgetItem.enterEvent(newEnter)
        item.widgetItem.mouseMoveEvent(newMove)
      else:
        if item.widgetItem.underMouse:
          newLeave = QEvent(TypeLeave)
          item.widgetItem.leaveEvent(newLeave)
    self.update()

  def mousePressEvent(self, event: QMouseEvent) -> None:
    """This method handles the mouse press event."""
    point = (event.points() or [None, ]).pop()
    if isinstance(point, QEventPoint):
      self.pressPosition = QEventPoint.lastPosition(point)
    else:
      self.pressPosition = QPointF(-1, -1)
    for item in self.getItems():
      rect = self.getRect(item)
      if rect.contains(self.pressPosition):
        relPos = QPointF(self.pressPosition - rect.topLeft())
        btn = event.buttons()
        mdf = event.modifiers()
        newPress = QMouseEvent(TypePress, relPos, btn, btn, mdf)
        item.widgetItem.mousePressEvent(newPress)
        break
    else:
      BoxWidget.mousePressEvent(self, event)
    self.update()

  def mouseReleaseEvent(self, event: QMouseEvent) -> None:
    """This method handles the mouse release event."""
    point = (event.points() or [None, ]).pop()
    if isinstance(point, QEventPoint):
      p = QEventPoint.lastPosition(point)
    else:
      p = QPointF(-1, -1)
    for item in self.getItems():
      rect = self.getRect(item)
      if rect.contains(p):
        relPos = QPointF(p - rect.topLeft())
        newRelease = QMouseEvent(TypeRelease, relPos, event.buttons(),
                                 event.button(), event.modifiers())
        item.widgetItem.mouseReleaseEvent(newRelease)
        break
    else:
      BoxWidget.mouseReleaseEvent(self, event)
    self.update()
