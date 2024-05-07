"""FileMenu provides the file menu for the main application window. It
subclasses the AbstractMenu class. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QAction

from ezside.app.menus import AbstractMenu


class FileMenu(AbstractMenu):
  """FileMenu provides the file menu for the main application window. It
  subclasses the AbstractMenu class. """

  new: QAction
  open: QAction
  save: QAction
  saveAs: QAction
  exit: QAction

  def initUi(self) -> None:
    """Initialize the user interface."""
    self.new = self.addAction(self.tr('New'))
    self.open = self.addAction(self.tr('Open'))
    self.save = self.addAction(self.tr('Save'))
    self.saveAs = self.addAction(self.tr('Save As'))
    self.exit = self.addAction(self.tr('Exit'))
