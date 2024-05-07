"""DebugWindow subclasses the MainWindow class allowing for debugging."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QWidget
from icecream import ic

from ezside.app import MainWindow

ic.configureOutput(includeContext=True, )


class DebugWindow(MainWindow):
  """DebugWindow subclasses the MainWindow class allowing for debugging."""

  __debug_flag__ = True

  def initSignalSlot(self) -> None:
    """Initialize the actions."""
    MainWindow.initSignalSlot(self)
    self.mainMenuBar.debug.debug1.triggered.connect(self.debug1Func)
    self.mainMenuBar.debug.debug2.triggered.connect(self.debug2Func)
    self.mainMenuBar.debug.debug3.triggered.connect(self.debug3Func)
    self.mainMenuBar.debug.debug4.triggered.connect(self.debug4Func)
    self.mainMenuBar.debug.debug5.triggered.connect(self.debug5Func)
    self.mainMenuBar.debug.debug6.triggered.connect(self.debug6Func)
    self.mainMenuBar.debug.debug7.triggered.connect(self.debug7Func)
    self.mainMenuBar.debug.debug8.triggered.connect(self.debug8Func)
    self.mainMenuBar.debug.debug9.triggered.connect(self.debug9Func)

  def debug1Func(self, ) -> None:
    """Debug1 function."""
    note = 'Debug1 function called'
    print(note)
    self.statusBar().showMessage(note)
    QWidget.adjustSize(self.sevenSegDisplay)
    QWidget.update(self.sevenSegDisplay)

  def debug2Func(self, ) -> None:
    """Debug2 function."""
    note = 'Debug2 function called'
    print(note)
    self.statusBar().showMessage(note)

  def debug3Func(self, ) -> None:
    """Debug3 function."""
    note = 'Debug3 function called'
    print(note)
    self.statusBar().showMessage(note)

  def debug4Func(self, ) -> None:
    """Debug4 function."""
    note = 'Debug4 function called'
    print(note)
    self.statusBar().showMessage(note)

  def debug5Func(self, ) -> None:
    """Debug5 function."""
    note = 'Debug5 function called'
    print(note)
    self.statusBar().showMessage(note)

  def debug6Func(self, ) -> None:
    """Debug6 function."""
    note = 'Debug6 function called'
    print(note)
    self.statusBar().showMessage(note)

  def debug7Func(self, ) -> None:
    """Debug7 function."""
    note = 'Debug7 function called'
    print(note)
    self.statusBar().showMessage(note)

  def debug8Func(self, ) -> None:
    """Debug8 function."""
    note = 'Debug8 function called'
    print(note)
    self.statusBar().showMessage(note)

  def debug9Func(self, ) -> None:
    """Debug9 function."""
    note = 'Debug9 function called'
    print(note)
    self.statusBar().showMessage(note)
