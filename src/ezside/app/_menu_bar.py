"""MenuBar provides the menu bar for the application."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QMenuBar
from worktoy.desc import AttriBox

from ezside.app import FileMenu


class MenuBar(QMenuBar):
  """MenuBar provides the menu bar for the application."""

  fileMenu = AttriBox[FileMenu]()

  def initUi(self) -> None:
    """Initializes the menu bar"""
    self.fileMenu.initUi()
    QMenuBar.addMenu(self, self.fileMenu)
