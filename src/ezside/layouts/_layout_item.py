"""LayoutItem represents a single item in a layout."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QSizeF, QSize
from worktoy.desc import AttriBox, Field, NODEF
from worktoy.meta import BaseObject, overload
from worktoy.text import typeMsg

from ezside.layouts import LayoutIndex
from ezside.widgets import BoxWidget


class LayoutItem(BaseObject):
  """BaseObject allows use of function overloading. """

  index: LayoutIndex

  __widget_item__ = None

  index = AttriBox[LayoutIndex](NODEF)
  widgetItem = Field()
  height = Field()  # Reflects the 'requiredSize' method on the widget
  width = Field()
  size = Field()

  @size.GET
  def _getSizeF(self) -> QSizeF:
    """Getter-function for the sizeF"""
    out = self.widgetItem.requiredSize()
    if isinstance(out, QSizeF):
      return out
    if isinstance(out, QSize):
      return QSize.toSizeF(out)
    e = typeMsg('requiredSize', out, QSizeF)
    raise TypeError(e)

  @height.GET
  def _getHeight(self) -> float:
    """Getter-function for the height"""
    return self.size.height()

  @width.GET
  def _getWidth(self) -> float:
    """Getter-function for the width"""
    return self.size.width()

  @widgetItem.SET
  def _setWidgetItem(self, widgetItem: BoxWidget) -> None:
    """Setter-function for the widget item"""
    if not isinstance(widgetItem, BoxWidget):
      e = typeMsg('widgetItem', widgetItem, BoxWidget)
      raise TypeError(e)
    self.__widget_item__ = widgetItem

  @widgetItem.GET
  def _getWidgetItem(self) -> BoxWidget:
    """Getter-function for the widget item"""
    if self.__widget_item__ is None:
      e = """The widget item has not been set!"""
      raise AttributeError(e)
    if not isinstance(self.__widget_item__, BoxWidget):
      e = typeMsg('widgetItem', self.__widget_item__, BoxWidget)
      raise TypeError(e)
    return self.__widget_item__

  @overload(LayoutIndex, BoxWidget)
  def __init__(self, index: LayoutIndex, widgetItem: BoxWidget) -> None:
    """Constructor for the LayoutItem class."""
    self.index = index
    self.widgetItem = widgetItem

  @overload(BoxWidget, LayoutIndex)
  def __init__(self, widgetItem: BoxWidget, index: LayoutIndex) -> None:
    """Constructor for the LayoutItem class."""
    self.index = index
    self.widgetItem = widgetItem

  @overload(int, int, BoxWidget)
  def __init__(self, row: int, col: int, widgetItem: BoxWidget) -> None:
    """Constructor for the LayoutItem class."""
    self.index = LayoutIndex(row, col)
    self.widgetItem = widgetItem

  @overload(BoxWidget, int, int)
  def __init__(self, widgetItem: BoxWidget, row: int, col: int) -> None:
    """Constructor for the LayoutItem class."""
    self.index = LayoutIndex(row, col)
    self.widgetItem = widgetItem

  @overload(int, BoxWidget, int)
  def __init__(self, row: int, widgetItem: BoxWidget, col: int) -> None:
    """Constructor for the LayoutItem class."""
    self.index = LayoutIndex(row, col)
    self.widgetItem = widgetItem

  @overload(tuple, BoxWidget)
  def __init__(self, index: tuple, widgetItem: BoxWidget) -> None:
    """Constructor for the LayoutItem class."""
    self.index = LayoutIndex(index)
    self.widgetItem = widgetItem

  @overload(BoxWidget, tuple)
  def __init__(self, widgetItem: BoxWidget, index: tuple) -> None:
    """Constructor for the LayoutItem class."""
    self.index = LayoutIndex(index)
    self.widgetItem = widgetItem

  @overload(list, BoxWidget)
  def __init__(self, index: list, widgetItem: BoxWidget) -> None:
    """Constructor for the LayoutItem class."""
    self.index = LayoutIndex(index)
    self.widgetItem = widgetItem

  @overload(BoxWidget, list)
  def __init__(self, widgetItem: BoxWidget, index: list) -> None:
    """Constructor for the LayoutItem class."""
    self.index = LayoutIndex(index)
    self.widgetItem = widgetItem
