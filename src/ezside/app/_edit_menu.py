"""EditMenu class provides the edit menu for the application."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox, THIS

from icecream import ic
from ezside.app import AbstractMenu, EZAction

ic.configureOutput(includeContext=True)


class EditMenu(AbstractMenu):
  """EditMenu class provides the edit menu for the application."""

  selectAllAction = AttriBox[EZAction](
      THIS, 'Select All', 'CTRL+A', 'select_all.png')
  copyAction = AttriBox[EZAction](THIS, 'Copy', 'CTRL+C', 'copy.png')
  cutAction = AttriBox[EZAction](THIS, 'Cut', 'CTRL+X', 'cut.png')
  pasteAction = AttriBox[EZAction](THIS, 'Paste', 'CTRL+V', 'paste.png')
  undoAction = AttriBox[EZAction](THIS, 'Undo', 'CTRL+Z', 'undo.png')
  redoAction = AttriBox[EZAction](THIS, 'Redo', 'CTRL+Y', 'redo.png')

  def initUi(self) -> None:
    """Initializes the menu"""
    self.addAction(self.selectAllAction)
    self.addAction(self.copyAction)
    self.addAction(self.cutAction)
    self.addAction(self.pasteAction)
    self.addAction(self.undoAction)
    self.addAction(self.redoAction)

  def __init__(self, parent=None, *args) -> None:
    AbstractMenu.__init__(self, parent, 'Edit')
    self.initUi()
