"""MainWindow subclasses the LayoutWindow and provides the main
application business logic."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic

from ezside.app import LayoutWindow

ic.configureOutput(includeContext=True, )


class MainWindow(LayoutWindow):
  """MainWindow subclasses the LayoutWindow and provides the main
  application business logic."""

  def initActions(self) -> None:
    """Initialize the actions."""

  def debug1Func(self, ) -> None:
    """Debug Function 1"""
    self.statusBar().showMessage('Debug Function 1')
    self.welcomeLabel.innerText += '*'
    self.welcomeLabel.update()

  def debug2Func(self) -> None:
    """Debug Function 2"""
    self.statusBar().showMessage(self.welcomeLabel.innerText)
