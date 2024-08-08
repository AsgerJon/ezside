"""AbstractLayout provides an abstract baseclass for layouts. The direct
subclasses of QLayout are too difficult to manage. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import (QRectF, QSizeF, QPointF, QSize, QMarginsF,
                            QPoint, \
                            QRect, QEvent)
from PySide6.QtGui import QColor, QPaintEvent, QPainter, QMouseEvent, \
  QEnterEvent
from icecream import ic
from worktoy.desc import AttriBox, Field
from worktoy.text import typeMsg

from ezside.layouts import LayoutItem
from ezside.widgets import BoxWidget

ic.configureOutput(includeContext=True)


class AbstractLayout(BoxWidget):
  """Instead of subclassing QLayout, the class wraps an instance of
  QLayout and assigns it to itself. This allows it to properly implement
  the 'requiredSize' methods. """

  paddings: QMarginsF
  borders: QMarginsF
  margins: QMarginsF
  allMargins: QMarginsF

  __cursor_position__ = None
  __mouse_region__ = None
  __layout_items__ = None
  __iter_contents__ = None

  spacing = AttriBox[int](0)

  cursorPosition = Field()
  mouseRegion = Field()
  rowCount = Field()
  colCount = Field()

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
    return max([item.width for item in self.getItemsInCol(col)] or [-1, ])

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
    return max([item.height for item in self.getItemsInRow(row)] or [-1, ])

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

  def addWidget(self, widget: BoxWidget, row: int, col: int) -> None:
    """Subclasses are required to implement this method. After adding the
    widget, the widget should be returned. """
    layoutItem = LayoutItem(widget, row, col)
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

  def getSize(self, item: LayoutItem) -> QSizeF:
    """Getter-function for the size at given grid"""
    col = item.index.col
    row = item.index.row
    width = self.getColWidth(col)
    height = self.getRowHeight(row)
    return QSizeF(width, height)

  def getRect(self, item: LayoutItem) -> QRectF:  # this name lol
    """Getter-function for the layout rectangle. """
    col = item.index.col
    row = item.index.row
    left = self.getColLeft(col)
    top = self.getRowTop(row)
    size = self.getSize(item)
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
      out = out.united(self.getRect(item))
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
    self.__cursor_position__ = event.localPos()
    for item in self.getItems():
      rect = self.getRect(item)
      if rect.contains(self.cursorPosition):
        if not item.widgetItem.underMouse:
          enterObject = QEnterEvent(self.cursorPosition,
                                    self.cursorPosition,
                                    self.cursorPosition, )
          item.widgetItem.enterEvent(enterObject)
        item.widgetItem.mouseMoveEvent(event)
      else:
        if item.widgetItem.underMouse:
          leaveObject = QEvent(QEvent.Type.Leave)
          item.widgetItem.leaveEvent(leaveObject)
    self.update()

  def mousePressEvent(self, event: QMouseEvent) -> None:
    """This method handles the mouse press event."""
    for item in self.getItems():
      rect = self.getRect(item)
      if rect.contains(self.cursorPosition):
        item.widgetItem.mousePressEvent(event)
        break
    else:
      BoxWidget.mousePressEvent(self, event)
    self.update()

  def mouseReleaseEvent(self, event: QMouseEvent) -> None:
    """This method handles the mouse release event."""
    for item in self.getItems():
      rect = self.getRect(item)
      if rect.contains(self.cursorPosition):
        item.widgetItem.mouseReleaseEvent(event)
        break
    else:
      BoxWidget.mouseReleaseEvent(self, event)
    self.update()
