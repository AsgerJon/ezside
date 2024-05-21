"""CoreStatusBar provides the menu entry point for the status bar inheriting
from both QStatusBar and EZObject. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QStatusBar

from ezside.app import EZObject
from ezside.core import parseParent


class CoreStatusBar(QStatusBar, EZObject):
  """CoreStatusBar provides the menu entry point for the status bar
  inheriting
  from both QStatusBar and EZObject. """

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the CoreStatusBar."""
    parent = parseParent(*args, **kwargs)
    QStatusBar.__init__(self, parent)
    EZObject.__init__(self, *args, **kwargs)
