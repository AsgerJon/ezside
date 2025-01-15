"""MenuBar subclasses the QMenuBar providing the menu bar for the main
window."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QMenuBar, QWidget
from worktoy.desc import AttriBox, THIS
from . import FileMenu, EditMenu, HelpMenu


class MenuBar(QMenuBar):
  """MenuBar subclasses the QMenuBar providing the menu bar for the main
  window."""

  fileMenu = AttriBox[FileMenu](THIS)
  editMenu = AttriBox[EditMenu](THIS)
  helpMenu = AttriBox[HelpMenu](THIS)

  def __init__(self, *args) -> None:
    for arg in args:
      if isinstance(arg, QWidget):
        QMenuBar.__init__(self, arg)
        break
    else:
      QMenuBar.__init__(self)

  def initMenus(self, ) -> None:
    self.fileMenu.initActions()
    self.addMenu(self.fileMenu)
    self.editMenu.initActions()
    self.addMenu(self.editMenu)
    self.helpMenu.initActions()
    self.addMenu(self.helpMenu)
