"""HelpMenu provides a help menu for the main application window. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox, Instance

from ezside.app.menus import AbstractMenu, Action


class HelpMenu(AbstractMenu):
  """HelpMenu provides a help menu for the main application window. """

  aboutQtAction = AttriBox[Action](Instance, 'About Qt', icon='aboutQt')
  aboutPySide6Action = AttriBox[Action](Instance,
                                        'About PySide6',
                                        icon='about_py_side6')
  aboutCondaAction = AttriBox[Action](Instance,
                                      'About Conda',
                                      icon='aboutConda')
  aboutPythonAction = AttriBox[Action](Instance,
                                       'About Python',
                                       icon='aboutPython')

  def initUi(self) -> None:
    """Initialize the user interface."""
    self.addAction(self.aboutQtAction)
    self.addAction(self.aboutPySide6Action)
    self.addAction(self.aboutCondaAction)
    self.addAction(self.aboutPythonAction)
