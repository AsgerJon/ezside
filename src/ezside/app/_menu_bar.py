"""MenuBar provides the menu bar for the application."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QMenuBar, QWidget
from worktoy.desc import AttriBox

from ezside.app import FileMenu, DebugMenu, HelpMenu, EditMenu


class MenuBar(QMenuBar):
  """MenuBar provides the menu bar for the application."""

  fileMenu = AttriBox[FileMenu]()
  editMenu = AttriBox[EditMenu]()
  helpMenu = AttriBox[HelpMenu]()
  debugMenu = AttriBox[DebugMenu]()

  def initUi(self) -> None:
    """Initializes the menu bar"""
    self.addMenu(self.fileMenu)
    self.addMenu(self.editMenu)
    self.addMenu(self.helpMenu)
    self.addMenu(self.debugMenu)

  def __init__(self, parent: QWidget = None, *args) -> None:
    """Initializes the menu bar"""
    QMenuBar.__init__(self, parent)
    self.initUi()
