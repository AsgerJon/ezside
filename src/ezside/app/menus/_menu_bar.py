"""MenuBar provides the menu bar for the application."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QMenuBar, QWidget
from icecream import ic
from worktoy.desc import AttriBox, THIS

from ezside.app.menus import FileMenu, DebugMenu, HelpMenu, EditMenu

ic.configureOutput(includeContext=True)


class MenuBar(QMenuBar):
  """MenuBar provides the menu bar for the application."""
  __is_initialized__ = None

  fileMenu = AttriBox[FileMenu](THIS)
  editMenu = AttriBox[EditMenu](THIS)
  helpMenu = AttriBox[HelpMenu](THIS)
  debugMenu = AttriBox[DebugMenu](THIS)

  def initBar(self) -> None:
    """Initializes the menu bar"""
    self.fileMenu.initMenu()
    self.addMenu(self.fileMenu)
    self.editMenu.initMenu()
    self.addMenu(self.editMenu)
    self.helpMenu.initMenu()
    self.addMenu(self.helpMenu)
    self.debugMenu.initMenu()
    self.addMenu(self.debugMenu)
