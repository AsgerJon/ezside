"""HorizontalLayout subclasses AbstractLayout providing a single row
layout."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.parse import maybe

from ezside.layouts import AbstractLayout, LayoutItem
from ezside.basewidgets import BoxWidget


class HorizontalLayout(AbstractLayout):
  """HorizontalLayout subclasses AbstractLayout providing a single row
  layout."""

  __layout_items__ = None

  def __len__(self, ) -> int:
    """Return the number of basewidgets in the layout."""
    return len(self.getWidgets())

  def __bool__(self) -> bool:
    """Return True if the layout has basewidgets."""
    return True if self.__layout_items__ else False

  def getWidgets(self, ) -> list[LayoutItem]:
    """Getter-function for the basewidgets"""
    return maybe(self.__layout_items__, [])

  def addWidget(self, widget: BoxWidget) -> BoxWidget:
    """Adds all basewidgets to the same row. """
    existing = self.getWidgets()
    widgetItem = LayoutItem(widget, 0, len(self))
    self.__layout_items__ = [*existing, widgetItem]
    return widget
