"""AbstractLayout provides an abstract baseclass for layouts. The direct
subclasses of QLayout are too difficult to manage. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QRectF, QSizeF, QPointF, QSize, QMarginsF, QEvent
from PySide6.QtGui import QColor, QPaintEvent, QPainter, QPointerEvent
from worktoy.desc import AttriBox, Field
from worktoy.text import typeMsg

from ezside.layouts import LayoutItem, LayoutIndex
from ezside.basewidgets import BoxWidget, LayoutWidget

try:
  from icecream import ic

  ic.configureOutput(includeContext=True)
except ImportError:
  ic = lambda *__, **_: None

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

  __layout_items__ = None
  __iter_contents__ = None

  spacing = AttriBox[int](0)

  rowCount = Field()
  colCount = Field()

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

  def getItemCount(self) -> int:
    """Getter-function for number of items"""
    return len(self.getItems())

  def addWidget(self, widget: BoxWidget, *args) -> LayoutItem:
    """Subclasses are required to implement this method. Upon receiving a
    widget, this method is responsible for added the given widget.
    Subclasses are entirely free to implement this functionality. The
    'AbstractLayout' class does provide 'addWidgetItem' that adds an
    instance of 'LayoutItem' to the list of inner items. This class
    requires an instance of 'LayoutIndex' instance that specifies the
    index and spans of the widget. """

  def addWidgetItem(self, layoutItem: LayoutItem) -> LayoutItem:
    """This method adds the given 'LayoutItem' to the list of inner
    items. """
    if not isinstance(layoutItem, LayoutItem):
      e = typeMsg('layoutItem', layoutItem, LayoutItem)
      raise TypeError(e)
    itemWidget = layoutItem.widgetItem
    if not isinstance(itemWidget, LayoutWidget):
      e = typeMsg('itemWidget', itemWidget, LayoutWidget)
      raise TypeError(e)
    if itemWidget.parentLayout is not self:
      itemWidget.parentLayout = self
    if itemWidget.parentLayoutItem is not layoutItem:
      itemWidget.parentLayoutItem = layoutItem
    existingItems = self.getItems()
    self.__layout_items__ = [*existingItems, layoutItem]
    return layoutItem

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
      item.widgetItem.parentRect = rect
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
    if self.parentLayout is None:
      return QSizeF.toSize(self.requiredRect().size())

  def event(self, widgetEvent: QEvent) -> bool:
    """Event handler for the layout. It passes pointer events on to the
    widget whose assigned rectangle bounds the position of the event. """
    if isinstance(widgetEvent, QPointerEvent):
      if self.handleEvent(widgetEvent):
        return True
    return BoxWidget.event(self, widgetEvent)

  def handleEvent(self, widgetEvent: QPointerEvent) -> bool:
    """Handle the event. """
    if QPointerEvent.pointCount(widgetEvent) - 1:
      return False
    return self.handlePoint(widgetEvent)

  def handlePoint(self, pointerEvent: QPointerEvent) -> bool:
    """Handles the point received. """
    eventPoint = pointerEvent.point(0)
    for item in self.getItems():
      widget = item.widgetItem
      widget.update()
      rect = self.getRect(item)
      if rect.contains(eventPoint.pos()):
        returnVal = widget.handlePointerEvent(pointerEvent)
        return True if returnVal else False
    return False
