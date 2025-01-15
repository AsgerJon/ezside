"""FileMenu subclasses QMenu. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QMenu, QWidget
from worktoy.desc import AttriBox, THIS

from . import AbstractAction


class FileMenu(QMenu):
  """FileMenu subclasses QMenu. """

  newAction = AttriBox[AbstractAction](THIS, 'New', 'Ctrl+N')
  openAction = AttriBox[AbstractAction](THIS, 'Open', 'Ctrl+O')
  saveAction = AttriBox[AbstractAction](THIS, 'Save', 'Ctrl+S')
  saveAsAction = AttriBox[AbstractAction](THIS, 'Save As', 'Ctrl+Shift+S')
  exitAction = AttriBox[AbstractAction](THIS, 'Exit', 'ALT+F4')

  def __init__(self, parent: QWidget) -> None:
    QMenu.__init__(self, parent)
    self.setTitle('File')

  def initActions(self, ) -> None:
    QMenu.addAction(self, self.newAction)
    QMenu.addAction(self, self.openAction)
    QMenu.addAction(self, self.saveAction)
    QMenu.addAction(self, self.saveAsAction)
    QMenu.addAction(self, self.exitAction)
