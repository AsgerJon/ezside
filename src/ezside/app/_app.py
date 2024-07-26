"""App subclasses the QApplication class."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import Qt, QThread, QSettings
from PySide6.QtWidgets import QApplication, QMainWindow
from icecream import ic
from worktoy.desc import EmptyField
from worktoy.parse import maybe
from worktoy.text import typeMsg

ic.configureOutput(includeContext=True, )

MenuFlag = Qt.ApplicationAttribute.AA_DontUseNativeMenuBar

if TYPE_CHECKING:
  pass


class App(QApplication):
  """App is a subclass of QApplication."""

  __main_window_class__ = None  # QMainWindow
  __main_window_instance__ = None

  mainWindow = EmptyField()

  def __init__(self, *args) -> None:
    cls, appArgs = None, None
    for arg in args:
      if isinstance(arg, type):
        if issubclass(arg, QMainWindow):
          cls = arg
      elif isinstance(arg, list):
        appArgs = arg
    QApplication.__init__(self, maybe(appArgs, []))
    if not issubclass(cls, QMainWindow):
      e = """The class must be a subclass of QMainWindow!"""
      raise TypeError(e)
    if cls is not None:
      self.setMainWindowClass(cls)

  def setMainWindowClass(self, cls: type) -> None:
    """Setter-function for the main window class."""
    if self.__main_window_class__ is not None:
      e = """Main window class already exists!"""
      raise AttributeError(e)
    if not issubclass(cls, QMainWindow):
      e = """The class must be a subclass of QMainWindow!"""
      raise TypeError(e)
    self.__main_window_class__ = cls

  def _createMainWindow(self) -> None:
    """Creator-function for the main window instance."""
    if self.__main_window_instance__ is not None:
      e = """Main window instance already exists!"""
      raise AttributeError(e)
    cls = self.__main_window_class__
    if cls is None:
      e = """Unable to resolve main window class!"""
      raise RuntimeError(e)
    if not issubclass(cls, QMainWindow):
      e = """The class must be a subclass of QMainWindow!"""
      raise TypeError(e)
    self.__main_window_instance__ = cls()

  @mainWindow.GET
  def _getMain(self, **kwargs) -> QMainWindow:
    """Getter-function for the main window instance. """
    if self.__main_window_instance__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createMainWindow()
      return self._getMain(_recursion=True)
    if isinstance(self.__main_window_instance__, QMainWindow):
      return self.__main_window_instance__
    e = typeMsg('mainWindow', self.__main_window_instance__, QMainWindow)
    raise TypeError(e)

  def closeThreads(self, ) -> None:
    """Method responsible for closing threads. """

  def getThreads(self, ) -> list[QThread]:
    """Method responsible for getting threads."""

  def registerThread(self, thread: QThread) -> None:
    """Method responsible for registering threads."""

  def getSettings(self) -> QSettings:
    """Method responsible for getting settings."""
    return QSettings()

  def exec(self) -> int:
    """Method responsible for executing the application."""
    self.mainWindow.show()
    return QApplication.exec_(self)
