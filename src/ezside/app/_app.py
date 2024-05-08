"""App subclasses the QApplication class."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QApplication
from attribox import AttriBox
from icecream import ic

from ezside.app import DebugWindow

ic.configureOutput(includeContext=True, )

MenuFlag = Qt.ApplicationAttribute.AA_DontUseNativeMenuBar

if TYPE_CHECKING:
  from ezside.app import AppThread


class App(QApplication):
  """App is a subclass of QApplication."""
  __error_code__ = None
  __registered_threads__ = None

  requestQuit = Signal()
  demandQuit = Signal()
  threadsExited = Signal()

  mainWindow = AttriBox[DebugWindow]()

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the App instance."""
    QApplication.__init__(self, *args)
    self.setApplicationName('EZSide')
    self.setOrganizationName('EZ')
    self.setAttribute(MenuFlag, True)
    self.mainWindow.initUi()
    self.requestQuit.connect(self.initiateQuit)
    self.threadsExited.connect(self.quit)

  def _getErrorCode(self, ) -> int:
    """Get the error code."""
    return self.__error_code__

  def _setErrorCode(self, errorCode: int) -> None:
    """Set the error code."""
    self.__error_code__ = errorCode

  def runtimeError(self, ) -> None:
    """Handle a runtime error."""
    self._setErrorCode(2)
    self.maybeQuit()
    self.quit()

  def timeoutError(self, ) -> None:
    """Handle a timeout error."""
    self._setErrorCode(1)
    self.maybeQuit()
    self.demandQuit.emit()

  @Slot()
  def initiateQuit(self) -> None:
    """Initialize the quit signal."""
    self.mainWindow.close()
    self.requestQuit.emit()

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
    thread.errorExit.connect(self.timeoutError)
    thread.critExit.connect(self.runtimeError)
    self.requestQuit.connect(thread.initiateQuit)
    self.demandQuit.connect(thread.forceQuit)

  def _getRunningThreads(self, ) -> list[AppThread]:
    """Get the running threads."""
    registeredThreads = self._getRegisteredThreads()
    return [thread for thread in registeredThreads if thread.isRunning()]

  def exec(self) -> int:
    """Executes the application."""
    self.mainWindow.show()
    self.mainWindow.requestQuit.connect(self.requestQuit)
    returnCode = super().exec()
    errorCode = self._getErrorCode()
    if errorCode:
      return errorCode
    return returnCode
