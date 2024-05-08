"""App subclasses the QApplication class."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QApplication
from icecream import ic

from ezside.app import DebugWindow

ic.configureOutput(includeContext=True, )

MenuFlag = Qt.ApplicationAttribute.AA_DontUseNativeMenuBar

if TYPE_CHECKING:
  from ezside.app import AppThread


class App(QApplication):
  """App is a subclass of QApplication."""

  mainWindow: DebugWindow

  __running_threads__ = None

  quitRequested = Signal()
  threadsExited = Signal()

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the App instance."""
    QApplication.__init__(self, *args)
    self.setApplicationName('EZSide')
    self.setOrganizationName('EZ')
    self.setAttribute(MenuFlag, True)
    self.mainWindow = DebugWindow()
    self.quitRequested.connect(self.quit)

  @Slot()
  def maybeQuit(self, ) -> None:
    """Checks if any running threads are still running"""
    for thread in self._getRunningThreads():
      if thread.isRunning():
        return
    else:
      self.quitRequested.emit()

  def _getRunningThreads(self, ) -> list:
    """Get the running threads."""
    if self.__running_threads__ is None:
      self.__running_threads__ = []
    return self.__running_threads__

  def registerThread(self, thread: AppThread) -> None:
    """Register a thread."""
    self._getRunningThreads().append(thread)

  def exec(self) -> int:
    """Executes the application."""
    self.mainWindow.show()
    self.mainWindow.requestQuit.connect(self.quitRequested)
    return QApplication.exec_(self)
