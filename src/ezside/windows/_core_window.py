"""CoreWindow provides the entry point for the main window class. It inherits
from both QMainWindow and EZObject. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QMainWindow
from icecream import ic

from ezside.app import EZObject
from ezside.desc import parseParent

ic.configureOutput(includeContext=True)


class CoreWindow(QMainWindow, EZObject):
  """CoreWindow provides the entry point for the main window class. It
  inherits
  from both QMainWindow and EZObject. """

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the CoreWindow."""
    EZObject.__init__(self, *args, **kwargs)
    parent = parseParent(*args, **kwargs)
    QMainWindow.__init__(self, parent, )

  def initMenus(self) -> None:
    """Initializes the menus."""

  def initActions(self) -> None:
    """Initializes the actions."""

  def initUi(self) -> None:
    """Initializes the user interface."""

  def show(self) -> None:
    """Shows the main window."""
    self.initMenus()
    self.initActions()
    self.initUi()
    QMainWindow.show(self)
