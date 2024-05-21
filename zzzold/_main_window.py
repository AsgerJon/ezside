"""MainWindow subclasses the LayoutWindow and provides the main
application business logic."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from math import sin
import time

from PySide6.QtCore import QTimer, Signal, Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QColorDialog
from icecream import ic

from ezside.windows import LayoutWindow
from ezside.menus import EditMenu, FileMenu, HelpMenu, DebugMenu
from ezside.core import Precise
from ezside.dialogs import AbstractTalker

ic.configureOutput(includeContext=True, )
NativeCol = QColorDialog.ColorDialogOption.DontUseNativeDialog


class MainWindow(LayoutWindow):
  """MainWindow subclasses the LayoutWindow and provides the main
  application business logic."""

  talker: AbstractTalker

  fileMenu: FileMenu
  editMenu: EditMenu
  helpMenu: HelpMenu

  new: QAction
  open: QAction
  save: QAction
  saveAs: QAction
  preferences: QAction
  exit: QAction
  aboutQt: QAction
  aboutPySide6: QAction
  aboutConda: QAction
  aboutPython: QAction
  help: QAction
  undo: QAction
  redo: QAction
  selectAll: QAction
  copy: QAction
  cut: QAction
  paste: QAction

  __debug_flag__ = True
  debug1: QAction
  debug2: QAction
  debug3: QAction
  debug4: QAction
  debug5: QAction
  debug6: QAction
  debug7: QAction
  debug8: QAction
  debug9: QAction

  debug: DebugMenu

  talk = Signal(float)

  def __init__(self, *args, **kwargs) -> None:
    LayoutWindow.__init__(self, *args, **kwargs)
    self._timer = QTimer()
    self._timer.setInterval(50)
    self._timer.setTimerType(Precise)
    self._timer.setSingleShot(False)

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
    self._timer.timeout.connect(self.liveChart.updateValues)

  def receiveSample(self, data: float) -> None:
    """Receives the sample data and applies it to the live chart"""
    self.liveChart.append(data)

  @Slot()
  def talkFunc(self) -> None:
    """Talk function."""
    self.talk.emit(sin(time.time()))

  def debug1Func(self, *args) -> None:
    """Debug1 function."""
    note = 'Debug1 open talker'
    self.statusBar().showMessage(note)
    self.talker = AbstractTalker()
    self.talker.show()

  def debug2Func(self, ) -> None:
    """Debug2 update plot"""
    note = 'Debug2 function called'
    self.mainStatusBar.showMessage(note, )

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
