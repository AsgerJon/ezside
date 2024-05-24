"""CoreStatusBar provides the menu entry point for the status bar inheriting
from both QStatusBar and EZObject. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QShowEvent
from PySide6.QtWidgets import QStatusBar

from ezside.app import EZObject
from ezside.desc import parseParent


class CoreStatusBar(QStatusBar, EZObject):
  """CoreStatusBar provides the menu entry point for the status bar
  inheriting
  from both QStatusBar and EZObject. """

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the CoreStatusBar."""
    EZObject.__init__(self, *args, **kwargs)
    parent = parseParent(*args, **kwargs)
    QStatusBar.__init__(self, parent)

  def initUi(self) -> None:
    """Initializes the user interface."""
