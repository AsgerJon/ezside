"""App subclasses the QApplication class."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QApplication
from icecream import ic

from ezside.app import DebugWindow, AppSettings

ic.configureOutput(includeContext=True, )

MenuFlag = Qt.ApplicationAttribute.AA_DontUseNativeMenuBar

if TYPE_CHECKING:
  from ezside.app import AppThread


class App(QApplication):
  """App is a subclass of QApplication."""

  mainWindow: DebugWindow

  __registered_threads__ = None

  stopThreads = Signal()
  threadsExited = Signal()

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the App instance."""
    QApplication.__init__(self, *args)
    self.setApplicationName('EZSide')
    self.setOrganizationName('EZ')
    self.setAttribute(MenuFlag, True)

  @staticmethod
  def getSettings() -> AppSettings:
    """Get the application settings."""
    return AppSettings()

  @Slot()
  def initiateQuit(self) -> None:
    """Initialize the quit signal."""
    self.stopThreads.emit()

  @Slot()
  def maybeQuit(self, ) -> None:
    """Checks if any running threads are still running"""
    for thread in self._getRunningThreads():
      if thread.isRunning():
        return
    else:
      self.threadsExited.emit()

  def _getRegisteredThreads(self, ) -> list:
    """Get the registered threads."""
    if self.__registered_threads__ is None:
      self.__registered_threads__ = []
    return self.__registered_threads__

  def registerThread(self, thread: AppThread) -> None:
    """Register a thread."""
    self._getRegisteredThreads().append(thread)
    thread.finished.connect(self.maybeQuit)
    self.stopThreads.emit(thread.initiateQuit)

  def _getRunningThreads(self, ) -> list[AppThread]:
    """Get the running threads."""
    registeredThreads = self._getRegisteredThreads()
    return [thread for thread in registeredThreads if thread.isRunning()]

  def exec(self) -> int:
    """Executes the application."""
    self.mainWindow = DebugWindow()
    self.mainWindow.setWindowIcon(self.getSettings().value('icon/pogchamp'))
    self.mainWindow.show()
    self.mainWindow.requestQuit.connect(self.initiateQuit)
    return super().exec()
