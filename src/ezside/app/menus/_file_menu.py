"""FileMenu provides the file menu for the main application window. It
subclasses the AbstractMenu class. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic
from worktoy.desc import AttriBox, Instance

from ezside.app.menus import AbstractMenu, Action

ic.configureOutput(includeContext=True, )


class FileMenu(AbstractMenu):
  """FileMenu provides the file menu for the main application window. It
  subclasses the AbstractMenu class. """

  newAction = AttriBox[Action](Instance, 'New', 'CTRL+N', icon='new', )
  openAction = AttriBox[Action](Instance, 'Open', 'CTRL+O', icon='open', )
  saveAction = AttriBox[Action](Instance, 'Save', 'CTRL+S', icon='save', )
  saveAsAction = AttriBox[Action](Instance,
                                  'Save As',
                                  'F12',
                                  icon='save_as', )
  prefAction = AttriBox[Action](Instance, 'Preferences',
                                icon='preferences', )
  exitAction = AttriBox[Action](Instance, 'Exit', 'ALT+F4', icon='exit', )

  def initUi(self) -> None:
    """Initialize the user interface."""
    self.addAction(self.newAction)
    self.addAction(self.openAction)
    self.addSeparator()
    self.addAction(self.saveAction)
    self.addAction(self.saveAsAction)
    self.addSeparator()
    self.addAction(self.prefAction)
    self.addSeparator()
    self.addAction(self.exitAction)
