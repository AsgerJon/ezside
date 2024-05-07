"""BaseWindow provides the base class for the main application window. It
implements menus and actions for the application, leaving widgets for the
LayoutWindow class."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from random import randint
from typing import Any, Callable

from PySide6.QtCore import Signal, QUrl, Slot
from PySide6.QtGui import QDesktopServices, QAction
from PySide6.QtWidgets import QMainWindow, QApplication
from icecream import ic

from ezside.app import _AttriWindow
from ezside.app.menus import MainMenuBar, MainStatusBar

ic.configureOutput(includeContext=True, )


class BaseWindow(_AttriWindow):
  """BaseWindow class provides menus and actions for the application."""

  mainMenuBar: MainMenuBar
  mainStatusBar: MainStatusBar

  __debug_flag__ = None

  __is_initialized__ = None

  requestQuit = Signal()
  requestHelp = Signal()
  hoverText = Signal(str)

  @staticmethod
  def link(url: Any) -> Callable:
    """Link to a URL."""
    if isinstance(url, str):
      url = QUrl(url)

    def go() -> bool:
      """Opens link in external browser."""
      return QDesktopServices.openUrl(url)

    return go

  def show(self) -> None:
    """Show the window."""
    if self.__is_initialized__ is None:  # Initialize the menu bar
      self.menuBar()
      self.statusBar()
      self._initCoreConnections()
      self.initStyle()
      self.initUi()
      self.initSignalSlot()
      self.__is_initialized__ = True
    QMainWindow.show(self)

  def _initCoreConnections(self) -> None:
    """Initialize the core actions for the main window."""
    self.statusBar()
    self.statusBar().showMessage('Initiating core connections...')
    self.menuBar().file.exit.triggered.connect(self.requestQuit)
    self.menuBar().help.help.triggered.connect(self.requestHelp)
    self.menuBar().help.aboutQt.triggered.connect(QApplication.aboutQt)
    condaLink = self.link('https://conda.io')
    pythonLink = self.link('https://python.org')
    pysideLink = self.link('https://doc.qt.io/qtforpython/')
    helpLink = self.link('https://www.youtube.com/watch?v=l60MnDJklnM')
    self.menuBar().help.aboutConda.triggered.connect(condaLink)
    self.menuBar().help.aboutPython.triggered.connect(pythonLink)
    self.menuBar().help.aboutPySide6.triggered.connect(pysideLink)
    self.menuBar().help.help.triggered.connect(helpLink)
    self._connectHover()
    self.hoverText.connect(self._announceHover)

  def _hoverFactory(self, action: QAction) -> Callable:
    """Factory function for hover handlers"""

    def hoverHandler() -> None:
      """Handle hover events."""
      self.hoverText.emit(action.text())

    return hoverHandler

  def _connectHover(self, ) -> None:
    """Connects all hover actions to hover text"""
    for menu in self.menuBar():
      for action in menu:
        handle = self._hoverFactory(action)
        action.hovered.connect(handle)

  @Slot(str)
  def _announceHover(self, message) -> None:
    """Announce hover text."""
    self.statusBar().showMessage(message)

  @abstractmethod  # LayoutWindow
  def initStyle(self, ) -> None:
    """Initializes the style of the main window."""

  @abstractmethod  # LayoutWindow
  def initUi(self, ) -> None:
    """Initializes the user interface for the main window."""

  @abstractmethod  # MainWindow
  def initSignalSlot(self, ) -> None:
    """Initializes the signal slot for the main window."""

  def menuBar(self, **kwargs) -> MainMenuBar:
    """Getter-function for the menu bar."""
    try:
      return self.mainMenuBar
    except AttributeError as attributeError:
      if kwargs.get('_recursion', False):
        raise RecursionError from attributeError
      self.setMenuBar(MainMenuBar())
      return self.menuBar(_recursion=True)

  def setMenuBar(self, mainMenuBar: MainMenuBar) -> None:
    """Set the menu bar for the main window."""
    mainMenuBar.initStyle()
    mainMenuBar.initUi()
    if getattr(self, '__debug_flag__', None) is not None:
      mainMenuBar.initDebug()
    mainMenuBar.initSignalSlot()
    self.mainMenuBar = mainMenuBar
    QMainWindow.setMenuBar(self, mainMenuBar)

  def statusBar(self, **kwargs) -> MainStatusBar:
    """Getter-function for the status bar."""
    try:
      return self.mainStatusBar
    except AttributeError as attributeError:
      if kwargs.get('_recursion', False):
        raise RecursionError from attributeError
      self.setStatusBar(MainStatusBar(self))
      return self.statusBar(_recursion=True)

  def setStatusBar(self, mainStatusBar: MainStatusBar) -> None:
    """Set the status bar for the main window."""
    mainStatusBar.initUi()
    self.mainStatusBar = mainStatusBar
    QMainWindow.setStatusBar(self, mainStatusBar)

  def showEvent(self, *args) -> None:
    """Show the window."""
    QMainWindow.showEvent(self, *args)
    self.statusBar().showMessage('Ready')
