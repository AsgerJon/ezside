"""MainWindow provides the full implementation of the main application
window. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

import time
from enum import EnumType

from PySide6.QtCore import Qt, QPoint, Slot, QEvent
from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QWidget, QLayout

from . import LayoutWindow


class MainWindow(LayoutWindow):
  """The 'MainWindow' class provides the full implementation of the main
  application window. """

  def initLogic(self, ) -> None:
    """Connects signals and slots"""
    self.button.clicked.connect(self.onButtonClicked)
    self.button.pressHold.connect(self.onButtonPressHold)

  def onButtonClicked(self, ) -> None:
    """Slot for the button clicked event."""
    info = """Button clicked at: %s""" % time.ctime()
    self.status.showMessage(info, )

  def onButtonPressHold(self, ) -> None:
    """Slot for the button pressHold event."""
    info = """Button pressHold at: %s""" % time.ctime()
    self.status.showMessage(info, )
