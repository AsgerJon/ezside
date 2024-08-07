"""VerticalLayout provides a layout, which explicitly exposes its widgets.
"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.parse import maybe

from ezside.layouts import AbstractLayout, LayoutItem
from ezside.widgets import BoxWidget


class VerticalLayout(AbstractLayout):
  """VerticalLayout subclasses AbstractLayout providing a single column
  layout."""

  __layout_items__ = None

  def __len__(self, ) -> int:
    """Return the number of widgets in the layout."""
    return len(self.getWidgets())

  def __bool__(self) -> bool:
    """Return True if the layout has widgets."""
    return True if self.__layout_items__ else False

  def getWidgets(self, ) -> list[LayoutItem]:
    """Getter-function for the widgets"""
    return maybe(self.__layout_items__, [])

  def addWidget(self, widget: BoxWidget) -> BoxWidget:
    """Adds all widgets to the same column. """
    existing = self.getWidgets()
    widgetItem = LayoutItem(widget, len(self), 0)
    self.__layout_items__ = [*existing, widgetItem]
    return widget
