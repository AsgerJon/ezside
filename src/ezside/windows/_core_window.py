"""CoreWindow provides the entry point for the main window class. It inherits
from both QMainWindow and EZObject. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QMainWindow

from ezside.app import EZObject
from ezside.core import parseParent


class CoreWindow(QMainWindow, EZObject):
  """CoreWindow provides the entry point for the main window class. It
  inherits
  from both QMainWindow and EZObject. """

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the CoreWindow."""
    parent = parseParent(*args, **kwargs)
    QMainWindow.__init__(self, parent)
    EZObject.__init__(self, *args, **kwargs)
