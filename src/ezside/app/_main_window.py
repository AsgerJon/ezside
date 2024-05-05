"""MainWindow subclasses the LayoutWindow and provides the main
application business logic."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QRect, QPoint, QPointF
from icecream import ic

from ezside.app import LayoutWindow

ic.configureOutput(includeContext=True, )


class MainWindow(LayoutWindow):
  """MainWindow subclasses the LayoutWindow and provides the main
  application business logic."""

  def initSignalSlot(self) -> None:
    """Initialize the actions."""

  def debug1Func(self, ) -> None:
    """Debug1Func provides a function for debugging."""
    ic('Debug1Func')
    self.statusBar().showMessage(str(self.menuBar()))
