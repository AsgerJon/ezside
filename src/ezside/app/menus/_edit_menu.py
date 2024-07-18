"""EditMenu provides the Edit menu for the main application. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox, Instance

from ezside.app.menus import AbstractMenu, Action


class EditMenu(AbstractMenu):
  """EditMenu provides the Edit menu for the main application. """

  selectAllAction = AttriBox[Action](Instance, 'Select All', 'CTRL+A',
                                     icon='select_all')
  copyAction = AttriBox[Action](Instance, 'Copy', 'CTRL+C', icon='copy')
  cutAction = AttriBox[Action](Instance, 'Cut', 'CTRL+X', icon='cut')
  pasteAction = AttriBox[Action](Instance, 'Paste', 'CTRL+V', icon='paste')
  undoAction = AttriBox[Action](Instance, 'Undo', 'CTRL+Z', icon='undo')
  redoAction = AttriBox[Action](Instance, 'Redo', 'CTRL+Y', icon='redo')

  def initUi(self) -> None:
    """Initialize the user interface."""
    self.addAction(self.selectAllAction)
    self.addSeparator()
    self.addAction(self.copyAction)
    self.addAction(self.cutAction)
    self.addAction(self.pasteAction)
    self.addSeparator()
    self.addAction(self.undoAction)
    self.addAction(self.redoAction)
