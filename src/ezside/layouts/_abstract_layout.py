"""AbstractLayout provides an abstract baseclass for layouts. The direct
subclasses of QLayout are too difficult to manage. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod

from PySide6.QtCore import QRectF, QSizeF, QPointF
from PySide6.QtGui import QColor, QPaintEvent, QPainter
from PySide6.QtWidgets import QWidget
from worktoy.desc import AttriBox, Field
from worktoy.text import monoSpace

from ezside.layouts import LayoutItem, LayoutIndex
from ezside.widgets import BoxWidget


class AbstractLayout(BoxWidget):
  """Instead of subclassing QLayout, the class wraps an instance of
  QLayout and assigns it to itself. This allows it to properly implement
  the 'requiredSize' methods. """

  __iter_contents__ = None

  spacing = AttriBox[int](0)

  rowCount = Field()
  colCount = Field()

  def getRowLeft(self, row: int) -> float:
    """Getter-function for the left side of the given row. """
    if row:
      return self.getRowLeft(row - 1) + self.getRowWidth(row - 1)
    return 0

  def getRowRight(self, row: int) -> float:
    """Getter-function for the right side of the given row"""
    return self.getRowLeft(row) + self.getRowWidth(row)

  def getColTop(self, col: int) -> float:
    """Getter-function for the top side of the given column"""
    if col:
      return self.getColTop(col - 1) + self.getColHeight(col - 1)
    return 0

  def getColBottom(self, col: int) -> float:
    """Getter-function for the bottom side of the given column"""
    return self.getColTop(col) + self.getColHeight(col)

  def getRowWidth(self, row: int) -> float:
    """Getter-function for the width of the given row. It is maximum width
    of the required sizes of the widgets. """
    out = 0
    oneSpan = False
    if row >= self.rowCount:
      e = """The row index: '%s' is out of bounds!""" % row
      raise IndexError(monoSpace(e))
    if row < 0:
      return self.getRowWidth(row + self.rowCount)
    for item in self:
      if item.index.row == row and item.index.rowSpan == 1:
        out = max(out, item.width)
        oneSpan = True
    if not oneSpan:
      for item in self:
        if item.index.row == row:
          item.index.rowSpan -= 1
      return self.getRowWidth(row)
    return out

  def getColHeight(self, col: int) -> float:
    """Getter-function for the height of the given column. It is maximum
    height of the required sizes of the widgets. """
    out = 0
    oneSpan = False
    if col >= self.colCount:
      e = """The column index: '%s' is out of bounds!""" % col
      raise IndexError(monoSpace(e))
    if col < 0:
      return self.getColHeight(col + self.colCount)
    for item in self:
      if item.index.col == col and item.index.colSpan == 1:
        out = max(out, item.height)
        oneSpan = True
    if not oneSpan:
      for item in self:
        if item.index.col == col:
          item.index.colSpan -= 1
      return self.getColHeight(col)
    return out

  @rowCount.GET
  def _getRowCount(self) -> int:
    """Getter-function for the row count attribute"""
    out = -1
    maxSpan = 1
    for item in self:
      if item.index.row > out:
        maxSpan = item.index.rowSpan
        out = item.index.row
    return out + maxSpan

  @colCount.GET
  def _getColCount(self) -> int:
    """Getter-function for the column count attribute"""
    out = -1
    maxSpan = 1
    for item in self:
      if item.index.col > out:
        maxSpan = item.index.colSpan
        out = item.index.col
    return out + maxSpan

  def __getitem__(self, *args) -> LayoutItem:
    """This method allows the user to access the layout items using
    square brackets. """
    for item in self:
      if item == args:
        return item
    e = """Unable to resolve the index: '%s' in the layout!""" % args
    raise IndexError(monoSpace(e))

  def __iter__(self) -> AbstractLayout:
    """This method implements the iteration protocol. """
    self.__iter_contents__ = [*self.getWidgets(), ]
    return self

  def __next__(self, ) -> LayoutItem:
    """This method implements the iteration protocol. """
    if self.__iter_contents__:
      return self.__iter_contents__.pop(0)
    raise StopIteration

  @abstractmethod
  def addWidget(self, *args) -> BoxWidget:
    """Subclasses are required to implement this method. After adding the
    widget, the widget should be returned. """

  @abstractmethod
  def getWidgets(self, ) -> list[LayoutItem]:
    """Subclasses are required to implement this method, to return the
    layoutItem representations of the widgets managed by the layout. This
    method is used by the iteration protocol implementation."""

  def __init__(self, *args) -> None:
    """This method initializes the layout. """
    self.margins = 2
    self.borders = 0
    self.paddings = 0
    self.borderColor = QColor(0, 0, 0, 255)
    self.backgroundColor = QColor(191, 191, 191, 255)

  def getSize(self, *args) -> QSizeF:
    """Getter-function for the size at given grid"""
    if len(args) == 1:
      if isinstance(args[0], LayoutItem):
        return self.getSize(args[0].index)
      if isinstance(args[0], LayoutIndex):
        return QSizeF(self.getRowWidth(args[0].row),
                      self.getColHeight(args[0].col))
    return self.getSize(LayoutIndex(*args))

  def getRect(self, *args) -> QRectF:  # this name lol
    """Getter-function for the layout rectangle. """
    if len(args) == 1:
      if isinstance(args[0], LayoutItem):
        return self.getRect(args[0].index)
      if isinstance(args[0], LayoutIndex):
        left = self.getRowLeft(args[0].row)
        top = self.getColTop(args[0].col)
        width, height = 0, 0

        size = QSizeF(width, height)
        topLeft = QPointF(left, top)
        return QRectF(topLeft, size)
    return self.getRect(LayoutIndex(*args))

  def paintEvent(self, event: QPaintEvent) -> None:
    """Reimplementation first painting self using parent method,
    then painting each widget. """
    BoxWidget.paintEvent(self, event)
    painter = QPainter()
    painter.begin(self)
    for item in self:
      rect = self.getRect(item.index)
      item.widgetItem.paintMeLike(rect, painter)
    painter.end()
