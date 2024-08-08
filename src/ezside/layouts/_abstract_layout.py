"""AbstractLayout provides an abstract baseclass for layouts. The direct
subclasses of QLayout are too difficult to manage. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import (QRectF, QSizeF, QPointF, QSize, QMarginsF,
                            QPoint, \
                            QRect, QEvent)
from PySide6.QtGui import QColor, QPaintEvent, QPainter, QMouseEvent, \
  QEnterEvent, QEventPoint
from icecream import ic
from worktoy.desc import AttriBox, Field
from worktoy.text import typeMsg

from ezside.layouts import LayoutItem, LayoutIndex
from ezside.basewidgets import BoxWidget

ic.configureOutput(includeContext=True)

TypePress = QEvent.Type.MouseButtonPress
TypeRelease = QEvent.Type.MouseButtonRelease
TypeMouseMove = QEvent.Type.MouseMove
TypeEnter = QEvent.Type.Enter
TypeLeave = QEvent.Type.Leave


class AbstractLayout(BoxWidget):
  """Instead of subclassing QLayout, the class wraps an instance of
  QLayout and assigns it to itself. This allows it to properly implement
  the 'requiredSize' methods. """

  paddings: QMarginsF
  borders: QMarginsF
  margins: QMarginsF
  allMargins: QMarginsF

  __cursor_position__ = None
  __press_position__ = None
  __mouse_region__ = None
  __layout_items__ = None
  __iter_contents__ = None

  spacing = AttriBox[int](0)

  cursorPosition = Field()
  pressPosition = Field()
  mouseRegion = Field()
  rowCount = Field()
  colCount = Field()

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

  def getColRight(self, col: int) -> float:
    """Return the right of the given column."""
    return self.getColLeft(col) + self.getColWidth(col)

  def getColLeft(self, col: int) -> float:
    """Return the left of the given column."""
    if col:
      return self.getColLeft(col - 1) + self.getColWidth(col - 1)
    return self.allMargins.left()

  def getColWidth(self, col: int) -> float:
    """Return the width of the given column."""
    out = 0
    for item in self.getItems():
      if item.index.col == col:
        if item.index.colSpan == 1:
          out = max(out, item.width)
    return out

  def getRowBottom(self, row: int) -> float:
    """Return the bottom of the given row."""
    return self.getRowTop(row) + self.getRowHeight(row)

  def getRowTop(self, row: int) -> float:
    """Return the top of the given row."""
    if row:
      return self.getRowTop(row - 1) + self.getRowHeight(row - 1)
    return self.allMargins.top()

  def getRowHeight(self, row: int) -> float:
    """Return the width of the given row."""
    out = 0
    for item in self.getItems():
      if item.index.row == row:
        if item.index.rowSpan == 1:
          out = max(out, item.height)
    return out

  def getItemsInRow(self, row: int) -> list[LayoutItem]:
    """Return the items in the given row."""
    return [item for item in self.getItems() if item.index.row == row]

  def getItemsInCol(self, col: int) -> list[LayoutItem]:
    """Return the items in the given column."""
    return [item for item in self.getItems() if item.index.col == col]

  @rowCount.GET
  def _getRowCount(self) -> int:
    """Getter-function for the row count attribute"""
    rows = [item.index.row for item in self.getItems()] or []
    return len(list(set(rows)))

  @colCount.GET
  def _getColCount(self) -> int:
    """Getter-function for the column count attribute"""
    cols = [item.index.col for item in self.getItems()] or []
    return len(list(set(cols)))

  def getItems(self) -> list[LayoutItem]:
    """Getter-function for the items"""
    return self.__layout_items__ or []

  def addWidget(self, widget: BoxWidget, row: int, col: int, *args) -> None:
    """Subclasses are required to implement this method. After adding the
    widget, the widget should be returned. """
    widget.parentLayout = self
    rowSpan, colSpan = [*args, 1, 1, ][:2]
    layoutIndex = LayoutIndex(row, col, rowSpan, colSpan)
    layoutItem = LayoutItem(widget, layoutIndex)
    widget.parentLayoutItem = layoutItem
    existing = self.__layout_items__ or []
    self.__layout_items__ = [*existing, layoutItem]

  def __init__(self, *args) -> None:
    """This method initializes the layout. """
    BoxWidget.__init__(self, *args)
    self.margins = 2
    self.borders = 1
    self.paddings = 2
    self.borderColor = QColor(0, 0, 0, 255)
    self.backgroundColor = QColor(255, 255, 0, 255)
    self.setMouseTracking(True)

  def getHeight(self, item: LayoutItem) -> float:
    """Getter-function for the height at given grid"""
    height = 0
    for row in range(item.index.row, item.index.row + item.index.rowSpan):
      height += self.getRowHeight(row)
    return height

  def getWidth(self, item: LayoutItem) -> float:
    """Getter-function for the width at given grid"""
    width = 0
    for col in range(item.index.col, item.index.col + item.index.colSpan):
      width += self.getColWidth(col)
    return width

  def getSize(self, item: LayoutItem) -> QSizeF:
    """Getter-function for the size at given grid"""
    width = self.getWidth(item)
    height = self.getHeight(item)
    return QSizeF(width, height)

  def getRect(self, item: LayoutItem) -> QRectF:  # this name lol
    """Getter-function for the layout rectangle. """
    col = item.index.col
    row = item.index.row
    left = self.getColLeft(col)
    top = self.getRowTop(row)
    size = self.getSize(item)
    reqSize = item.widgetItem.requiredSize()
    width = max(size.width(), reqSize.width())
    height = max(size.height(), reqSize.height())
    size = QSizeF(width, height)
    return QRectF(QPointF(left, top), size)

  def paintEvent(self, event: QPaintEvent) -> None:
    """Reimplementation first painting self using parent method,
    then painting each widget. """
    painter = QPainter()
    painter.begin(self)
    viewRect = painter.viewport()
    reqRect = self.requiredRect()
    BoxWidget.paintMeLike(self, reqRect, painter)
    for item in self.getItems():
      rect = self.getRect(item)
      item.widgetItem.paintMeLike(rect, painter)
    painter.end()

  def requiredSize(self) -> QSizeF:
    """Return the required size. """
    return self.requiredRect().size()

  def requiredRect(self) -> QRectF:
    """Return the required rectangle. """
    out = QRectF()
    for item in self.getItems():
      size = item.widgetItem.requiredSize()
      topLeft = self.getRect(item).topLeft()
      out = out.united(QRectF(topLeft, size))
    return out + self.allMargins

  def minimumSizeHint(self) -> QSize:
    """Return the minimum size hint. """
    return QSizeF.toSize(self.requiredRect().size())

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
