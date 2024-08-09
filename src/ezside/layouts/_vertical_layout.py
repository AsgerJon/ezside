"""VerticalLayout provides a layout, which explicitly exposes its
basewidgets.
"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic
from worktoy.parse import maybe

from ezside.layouts import AbstractLayout, LayoutItem, LayoutIndex
from ezside.basewidgets import BoxWidget


class VerticalLayout(AbstractLayout):
  """VerticalLayout subclasses AbstractLayout providing a single column
  layout."""

  def addWidget(self, widget: BoxWidget, *args) -> LayoutItem:
    """Add a widget to the layout."""
    index = LayoutIndex(self.getItemCount(), 0)
    layoutItem = LayoutItem(widget, index)
    self.addWidgetItem(layoutItem)
    return layoutItem
