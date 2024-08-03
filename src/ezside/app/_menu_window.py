"""MenuWindow implements menus as distinct classes."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QMainWindow
from worktoy.desc import AttriBox

from ezside.app import MenuBar


class MenuWindow(QMainWindow):
  """MenuWindow implements menus as distinct classes."""

  menuBar = AttriBox[MenuBar]()

  def initUi(self) -> None:
    """Initializes the main window"""
    self.setMenuBar(self.menuBar)
    self.menuBar.initUi()

  def show(self) -> None:
    """Shows the main window"""
    self.initUi()
    QMainWindow.show(self)
