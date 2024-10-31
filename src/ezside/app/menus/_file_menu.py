"""FileMenu subclasses the QMenu class and provides the file menu for the
main window. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QWidget, QMenu
from icecream import ic
from worktoy.desc import AttriBox, THIS

from ezside.app.menus import EZMenu, EZAction

ic.configureOutput(includeContext=True)


class FileMenu(EZMenu):
  """FileMenu subclasses the QMenu class and provides the file menu for the
  main window. """

  newAction = AttriBox[EZAction](THIS, 'New', 'CTRL+N', 'new')
  openAction = AttriBox[EZAction](THIS, 'Open', 'CTRL+O', 'open')
  saveAction = AttriBox[EZAction](THIS, 'Save', 'CTRL+S', 'save')
  saveAsAction = AttriBox[EZAction](
      THIS, 'Save As', 'CTRL+SHIFT+S', 'saveAs')
  exitAction = AttriBox[EZAction](THIS, 'Exit', 'CTRL+Q', 'exit')

  def initMenu(self) -> None:
    """Initializes the menu"""
    self.addAction(self.newAction)
    self.addAction(self.openAction)
    self.addAction(self.saveAction)
    self.addAction(self.saveAsAction)
    self.addAction(self.exitAction)
