"""HorizontalLayout subclasses AbstractLayout providing a single row
layout."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ezside.layouts import AbstractLayout
from ezside.base_widgets import BoxWidget, LayoutWidget


class HorizontalLayout(AbstractLayout):
  """HorizontalLayout subclasses AbstractLayout providing a single row
  layout."""

  def addWidget(self, widget: BoxWidget, *args) -> LayoutWidget:
    """Add a widget to the layout."""
    row, col = 0, self.getItemCount()
    return AbstractLayout.addWidget(self, widget, row, col)
