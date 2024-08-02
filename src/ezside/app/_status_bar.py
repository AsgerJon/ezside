"""StatusBar subclasses QStatusBar providing the status bar for the main
window application."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QShowEvent
from PySide6.QtWidgets import QStatusBar, QMainWindow, QHBoxLayout, QLabel
from worktoy.desc import AttriBox

from ezside.widgets import DigitalClock


class StatusBar(QStatusBar):
  """StatusBar subclasses QStatusBar providing the status bar for the main
  window application."""

  digitalClock = AttriBox[DigitalClock]()

  def __init__(self, *args) -> None:
    for arg in args:
      if isinstance(arg, QMainWindow):
        QStatusBar.__init__(self, arg)
        break
    else:
      QStatusBar.__init__(self)
    self.digitalClock.refreshTime()
    QStatusBar.addPermanentWidget(self, self.digitalClock)
    QStatusBar.setSizeGripEnabled(self, True)

  def showEvent(self, event: QShowEvent) -> None:
    """Show the main window."""
    QMainWindow.showEvent(self, event)
    print('%s - Show event' % self.__class__.__name__)
