"""MainWindow subclasses the LayoutWindow and provides the main
application business logic."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QColorDialog
from icecream import ic

from ezside.app import LayoutWindow
from ezside.app.menus import EditMenu, FileMenu, HelpMenu, DebugMenu

ic.configureOutput(includeContext=True, )
NativeCol = QColorDialog.ColorDialogOption.DontUseNativeDialog


class MainWindow(LayoutWindow):
  """MainWindow subclasses the LayoutWindow and provides the main
  application business logic."""

  __debug_flag__ = True

  def initSignalSlot(self) -> None:
    """Initialize the actions."""
    LayoutWindow.initSignalSlot(self)
    self.debug1.triggered.connect(self.debug1Func)
    self.debug2.triggered.connect(self.debug2Func)
    self.debug3.triggered.connect(self.debug3Func)
    self.debug4.triggered.connect(self.debug4Func)
    self.debug5.triggered.connect(self.debug5Func)
    self.debug6.triggered.connect(self.debug6Func)
    self.debug7.triggered.connect(self.debug7Func)
    self.debug8.triggered.connect(self.debug8Func)
    self.debug9.triggered.connect(self.debug9Func)
    self.titleWidget.initSignalSlot()
    self.liveChart.initSignalSlot()

  def debug1Func(self, *args) -> None:
    """Debug1 function."""
    note = 'Debug1 function called'
    self.statusBar().showMessage(note)
    self.colorDialog.show()

  def debug2Func(self, ) -> None:
    """Debug2 function."""
    note = 'Debug2 function called'
    self.mainStatusBar.showMessage(note, )
    self.fontDialog.show()

  def debug3Func(self, *args) -> None:
    """Debug3 function."""
    note = 'Debug3 function called'
    self.statusBar().showMessage(note)
    self.openFileDialog.show()

  def debug4Func(self, ) -> None:
    """Debug4 function."""
    note = 'Debug4 function called'
    self.statusBar().showMessage(note)
    self.saveFileDialog.show()

  def debug5Func(self, ) -> None:
    """Debug5 function."""
    note = 'Debug5 function called'
    print(note)
    self.statusBar().showMessage(note)
    self.folderDialog.show()

  def debug6Func(self, ) -> None:
    """Debug6 function."""
    note = 'Debug6 function called'
    print(note)
    self.statusBar().showMessage(note)
    self.cunt.show()

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
