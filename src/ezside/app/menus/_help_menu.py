"""HelpMenu provides the help menu for the application. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic
from worktoy.desc import AttriBox, THIS

from ezside.app.menus import EZMenu, EZAction

ic.configureOutput(includeContext=True)


class HelpMenu(EZMenu):
  """The 'HelpMenu' class provides the help menu for the application. """

  aboutQtAction = AttriBox[EZAction](THIS, 'About Qt', 'F12', 'qt')
  aboutPythonAction = AttriBox[EZAction](
      THIS, 'About Python', 'F11', 'python')
  aboutPySide6Action = AttriBox[EZAction](
      THIS, 'About PySide6', 'F10', 'pyside6')
  docAction = AttriBox[EZAction](THIS, 'Documentation', 'F1', 'doc')

  def initMenu(self) -> None:
    """Initializes the menu"""
    self.addAction(self.aboutQtAction)
    self.addAction(self.aboutPythonAction)
    self.addAction(self.aboutPySide6Action)
    self.addAction(self.docAction)
