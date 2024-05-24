"""CoreMenuBar provides the menu bar entry point for menus inheriting from
both QMenuBar and EZObject. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QMenuBar

from ezside.app import EZObject
from ezside.desc import parseParent


class CoreMenuBar(QMenuBar, EZObject):
  """CoreMenuBar provides the menu bar entry point for menus inheriting from
  both QMenuBar and EZObject. """

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the CoreMenuBar."""
    parent = parseParent(*args, **kwargs)
    EZObject.__init__(self, *args, **kwargs)
    QMenuBar.__init__(self, parent)

  def initUi(self) -> None:
    """Initializes the user interface."""
