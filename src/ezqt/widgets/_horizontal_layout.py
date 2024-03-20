"""Horizontal layout widget."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout

from ezqt.widgets import BoxLayout


class HLayout(BoxLayout):
  """Horizontal layout widget."""

  def createBaseLayout(self) -> None:
    """Creates the base layout."""
    self.setBaseLayout(QHBoxLayout())
