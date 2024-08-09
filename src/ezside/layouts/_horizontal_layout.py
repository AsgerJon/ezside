"""HorizontalLayout subclasses AbstractLayout providing a single row
layout."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.parse import maybe

from ezside.layouts import AbstractLayout, LayoutItem, LayoutIndex
from ezside.basewidgets import BoxWidget


class HorizontalLayout(AbstractLayout):
  """HorizontalLayout subclasses AbstractLayout providing a single row
  layout."""

  def addWidget(self, widget: BoxWidget, *args) -> LayoutItem:
    """Add a widget to the layout."""
    index = LayoutIndex(0, self.getItemCount())
    layoutItem = LayoutItem(widget, index)
    self.addWidgetItem(layoutItem)
    return layoutItem
