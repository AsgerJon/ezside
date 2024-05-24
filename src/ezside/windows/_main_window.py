"""MainWindow class for the main window of the application."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Slot
from PySide6.QtGui import QFont
from icecream import ic

from ezside.windows import LayoutWindow

ic.configureOutput(includeContext=True)


class MainWindow(LayoutWindow):
  """MainWindow class for the main window of the application."""

  @Slot(QFont)
  def onFontSelected(self, font: QFont) -> None:
    """Handles the font selected event."""
    self.welcomeLabel.font = font
    self.welcomeLabel.adjustSize()
    self.welcomeLabel.update()
    self.welcomeLabel.adjustSize()
    self.baseWidget.update()
    self.update()
    self.baseWidget.update()
    self.update()
