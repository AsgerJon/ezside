"""EditMenu class provides the edit menu for the application."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox

from ezside.app import AbstractMenu, EZAction


class EditMenu(AbstractMenu):
  """EditMenu class provides the edit menu for the application."""

  selectAllAction = AttriBox[EZAction](
      'Select All', 'CTRL+A', 'select_all.png')
  copyAction = AttriBox[EZAction]('Copy', 'CTRL+C', 'copy.png')
  cutAction = AttriBox[EZAction]('Cut', 'CTRL+X', 'cut.png')
  pasteAction = AttriBox[EZAction]('Paste', 'CTRL+V', 'paste.png')
  undoAction = AttriBox[EZAction]('Undo', 'CTRL+Z', 'undo.png')
  redoAction = AttriBox[EZAction]('Redo', 'CTRL+Y', 'redo.png')

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
