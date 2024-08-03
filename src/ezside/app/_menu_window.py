"""MenuWindow implements menus as distinct classes."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QMainWindow
from icecream import ic
from worktoy.desc import AttriBox

from ezside.app import MenuBar

ic.configureOutput(includeContext=True)


class MenuWindow(QMainWindow):
  """MenuWindow implements menus as distinct classes."""

  mainMenuBar = AttriBox[MenuBar]()

  def __init__(self) -> None:
    """Initializes the menu window"""
    QMainWindow.__init__(self)
    self.setWindowTitle('Menu Window')
    self.setMenuBar(self.mainMenuBar)
