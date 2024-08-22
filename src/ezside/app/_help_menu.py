"""HelpMenu provides the help menu for the application. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic
from worktoy.desc import AttriBox, THIS

from ezside.app import EZAction, AbstractMenu

ic.configureOutput(includeContext=True)


class HelpMenu(AbstractMenu):
  """The 'HelpMenu' class provides the help menu for the application. """

  aboutQtAction = AttriBox[EZAction](THIS, 'About Qt', 'F12', 'about_qt.png')
  aboutPythonAction = AttriBox[EZAction](
      THIS, 'About Python', 'F11', 'about_python.png')
  aboutPySide6Action = AttriBox[EZAction](
      THIS, 'About PySide6', 'F10', 'about_pyside6.png')
  docAction = AttriBox[EZAction](THIS,
                                 'Documentation',
                                 'F1',
                                 'documentation.png')

  def initUi(self) -> None:
    """Initializes the menu"""
    self.addAction(self.aboutQtAction)
    self.addAction(self.aboutPythonAction)
    self.addAction(self.aboutPySide6Action)
    self.addAction(self.docAction)

  def __init__(self, parent=None, *args) -> None:
    AbstractMenu.__init__(self, parent, 'Help')
    self.initUi()
