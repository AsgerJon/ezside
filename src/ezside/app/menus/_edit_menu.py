"""EditMenu provides the Edit menu for the main application. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QAction

from ezside.app.menus import AbstractMenu


class EditMenu(AbstractMenu):
  """EditMenu provides the Edit menu for the main application. """

  selectAll: QAction
  copy: QAction
  cut: QAction
  paste: QAction
  undo: QAction
  redo: QAction

  def initUi(self) -> None:
    """Initialize the user interface."""
    self.selectAll = self.addAction(self.tr('Select All'))
    self.addSeparator()
    self.copy = self.addAction(self.tr('Copy'))
    self.cut = self.addAction(self.tr('Cut'))
    self.paste = self.addAction(self.tr('Paste'))
    self.addSeparator()
    self.undo = self.addAction(self.tr('Undo'))
    self.redo = self.addAction(self.tr('Redo'))
