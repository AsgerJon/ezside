"""VerticalLayout provides a layout, which explicitly exposes its
base_widgets.
"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ezside.layouts import AbstractLayout
from ezside.base_widgets import BoxWidget, LayoutWidget


class VerticalLayout(AbstractLayout):
  """VerticalLayout subclasses AbstractLayout providing a single column
  layout."""

  def addWidget(self, widget: BoxWidget, *args) -> LayoutWidget:
    """Add a widget to the layout."""
    row, col = self.getItemCount(), 0
    return AbstractLayout.addWidget(self, widget, row, col)
