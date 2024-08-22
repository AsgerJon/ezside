"""LayoutItem represents a single item in a layout."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QSizeF
from worktoy.desc import AttriBox, Field
from worktoy.meta import BaseObject
from worktoy.parse import maybeType

from ezside.layouts import LayoutIndex
from ezside.base_widgets import LayoutWidget


class LayoutItem(BaseObject):
  """BaseObject allows use of function overloading. """

  __layout_index__ = None
  __widget_item__ = None
  __under_mouse__ = False

  index = Field()
  widgetItem = Field()

  size = Field()
  height = Field()
  width = Field()

  @index.GET
  def _getIndex(self) -> LayoutIndex:
    """Getter-function for the index."""
    return self.__layout_index__

  @index.SET
  def _setIndex(self, index: LayoutIndex) -> None:
    """Setter-function for the index."""
    self.__layout_index__ = index

  @size.GET
  def _getSize(self) -> QSizeF:
    """Getter-function for the size."""
    return self.__widget_item__.requiredSize()

  @height.GET
  def _getHeight(self) -> float:
    """Getter-function for the height."""
    return self.size.height()

  @width.GET
  def _getWidth(self) -> float:
    """Getter-function for the width."""
    return self.size.width()

  @widgetItem.GET
  def _getWidgetItem(self) -> LayoutWidget:
    """Getter-function for the widgetItem."""
    return self.__widget_item__

  @widgetItem.SET
  def _setWidgetItem(self, widget: LayoutWidget) -> None:
    """Setter-function for the widgetItem."""
    self.__widget_item__ = widget

  def __init__(self, *args) -> None:
    self.__layout_index__ = maybeType(LayoutIndex, *args)
    self.__widget_item__ = maybeType(LayoutWidget, *args)

  def __str__(self) -> str:
    """String representation"""
    clsName = self.widgetItem.__class__.__name__
    return """%s at: %s""" % (clsName, self.index)

  def __repr__(self) -> str:
    """String representation"""
    clsName = self.widgetItem.__class__.__name__
    return """%s at: %s""" % (clsName, self.index)
