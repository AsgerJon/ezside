"""HelpMenu subclasses QMenu and provides the help menu for the main
application. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QMenu, QWidget
from worktoy.desc import AttriBox, THIS

from . import AbstractAction


class HelpMenu(QMenu):
  """HelpMenu subclasses QMenu and provides the help menu for the main
  application. """

  aboutQtAction = AttriBox[AbstractAction](THIS, 'About Qt', 'F12')

  def __init__(self, parent: QWidget) -> None:
    QMenu.__init__(self, parent)
    self.setTitle('Help')

  def initActions(self, ) -> None:
    QMenu.addAction(self, self.aboutQtAction)
