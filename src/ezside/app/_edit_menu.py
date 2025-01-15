"""EditMenu subclasses QMenu and provides the edit menu for the main
application. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QMenu, QWidget
from worktoy.desc import AttriBox, THIS

from . import AbstractAction


class EditMenu(QMenu):
  """EditMenu subclasses QMenu and provides the edit menu for the main
  application. """

  undoAction = AttriBox[AbstractAction](THIS, 'Undo', 'Ctrl+Z')
  redoAction = AttriBox[AbstractAction](THIS, 'Redo', 'Ctrl+Y')
  cutAction = AttriBox[AbstractAction](THIS, 'Cut', 'Ctrl+X')
  copyAction = AttriBox[AbstractAction](THIS, 'Copy', 'Ctrl+C')
  pasteAction = AttriBox[AbstractAction](THIS, 'Paste', 'Ctrl+V')
  selectAllAction = AttriBox[AbstractAction](THIS, 'Select All', 'Ctrl+A')

  def __init__(self, parent: QWidget) -> None:
    QMenu.__init__(self, parent)
    self.setTitle('Edit')

  def initActions(self, ) -> None:
    QMenu.addAction(self, self.undoAction)
    QMenu.addAction(self, self.redoAction)
    QMenu.addAction(self, self.cutAction)
    QMenu.addAction(self, self.copyAction)
    QMenu.addAction(self, self.pasteAction)
    QMenu.addAction(self, self.selectAllAction)
