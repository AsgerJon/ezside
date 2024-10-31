"""EditMenu class provides the edit menu for the application."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox, THIS

from icecream import ic
from ezside.app.menus import EZMenu, EZAction

ic.configureOutput(includeContext=True)


class EditMenu(EZMenu):
  """EditMenu class provides the edit menu for the application."""

  selectAllAction = AttriBox[EZAction](
      THIS, 'Select All', 'CTRL+A', 'selectAll')
  copyAction = AttriBox[EZAction](THIS, 'Copy', 'CTRL+C', 'copy')
  cutAction = AttriBox[EZAction](THIS, 'Cut', 'CTRL+X', 'cut')
  pasteAction = AttriBox[EZAction](THIS, 'Paste', 'CTRL+V', 'paste')
  undoAction = AttriBox[EZAction](THIS, 'Undo', 'CTRL+Z', 'undo')
  redoAction = AttriBox[EZAction](THIS, 'Redo', 'CTRL+Y', 'redo')

  def initMenu(self) -> None:
    """Initializes the menu"""
    self.addAction(self.selectAllAction)
    self.addAction(self.copyAction)
    self.addAction(self.cutAction)
    self.addAction(self.pasteAction)
    self.addAction(self.undoAction)
    self.addAction(self.redoAction)
