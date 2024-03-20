"""GridLayout widget implementation"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QGridLayout

from ezqt.widgets import BoxLayout


class GridLayout(BoxLayout):
  """GridLayout widget."""

  def createBaseLayout(self) -> None:
    """Creates the base layout."""
    self.setBaseLayout(QGridLayout())

  def addWidget(self, widget: BoxLayout, row: int, column: int) -> None:
    """Adds a widget to the layout."""
    self.__child_widgets__.append(widget)
    widget.initUi()
    widget.connectActions()
    self.getBaseLayout().addWidget(widget, row, column)
