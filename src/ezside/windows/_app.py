"""App subclasses QApplication and provides the main application object. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QApplication


class App(QApplication):
  """App subclasses QApplication and provides the main application
  object. """

  settings = App

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the App object."""
