"""MainStatusBar provides a status bar for the main application window."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QStatusBar, QWidget, QMainWindow
from attribox import AttriBox
from icecream import ic

from ezside.core import EZTimer, Coarse
from ezside.widgets import DigitalClock

ic.configureOutput(includeContext=True)


class MainStatusBar(QStatusBar):
  """StatusBar provides a status bar for the main application window."""

  digitalClock = AttriBox[DigitalClock]()
  refreshClock = AttriBox[EZTimer](250, Coarse, False)

  def initUi(self, ) -> None:
    """Initializes the user interface for the status bar."""
    self.setStyleSheet("""background-color: #e0e0e0; color: #000000;
    border-top: 1px solid #000000; border-left: 1px solid #000000;
    border-right: 1px solid #000000; border-bottom: 1px solid #000000;""")
    self.addPermanentWidget(self.digitalClock)
    self.digitalClock.initUi()
    self.refreshClock.timeout.connect(self.digitalClock.update)
    self.refreshClock.start()
