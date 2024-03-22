""" Vertical layout widget. """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QVBoxLayout

from ezside.widgets import BoxLayout


class VLayout(BoxLayout):
  """Horizontal layout widget."""

  def createBaseLayout(self) -> None:
    """Creates the base layout."""
    self.setBaseLayout(QVBoxLayout())
