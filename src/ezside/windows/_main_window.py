"""MainWindow subclasses the LayoutWindow and provides the main
application business logic."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow, QApplication
from icecream import ic
from attribox import AttriBox

from ezside.windows.bars import MenuBar, StatusBar
from ezside.core import Precise
from ezside.widgets import Timer
from ezside.windows import LayoutWindow
from ezside.settings import Default

ic.configureOutput(includeContext=True, )


class MainWindow(LayoutWindow):
  """MainWindow subclasses the LayoutWindow and provides the main
  application business logic."""

  def initActions(self) -> None:
    """Initialize the actions."""