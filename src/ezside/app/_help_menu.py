"""HelpMenu provides the help menu for the application. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox

from ezside.app import EZAction, AbstractMenu


class HelpMenu(AbstractMenu):
  """The 'HelpMenu' class provides the help menu for the application. """

  aboutQtAction = AttriBox[EZAction]('About Qt', 'F12', 'about_qt.png')
  aboutPythonAction = AttriBox[EZAction](
      'About Python', 'F11', 'about_python.png')
  aboutPySide6Action = AttriBox[EZAction](
      'About PySide6', 'F10', 'about_pyside6.png')
  docAction = AttriBox[EZAction]('Documentation', 'F1', 'doc.png')

  def initUi(self) -> None:
    """Initializes the menu"""
    self.addAction(self.aboutQtAction)
    self.addAction(self.aboutPythonAction)
    self.addAction(self.aboutPySide6Action)
    self.addAction(self.docAction)

  def __init__(self, parent=None, *args) -> None:
    AbstractMenu.__init__(self, parent, 'Help')
    self.initUi()
