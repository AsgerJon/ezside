"""BaseWindow provides the base class for the main application window. It
implements menus and actions for the application, leaving widgets for the
LayoutWindow class."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import Any, Callable

from PySide6.QtCore import QUrl, Slot, Signal
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QMainWindow, QApplication
from icecream import ic
from worktoy.desc import Instance, AttriBox

from ezside.app.menus import MainMenuBar, MainStatusBar

ic.configureOutput(includeContext=True, )


class BaseWindow(QMainWindow):
  """BaseWindow class provides menus and actions for the application."""

  __is_initialized__ = None
  __is_closing__ = False

  pulse = Signal()
  requestQuit = Signal()
  confirmQuit = Signal()
  requestHelp = Signal()

  mainMenuBar = AttriBox[MainMenuBar](Instance, )
  mainStatusBar = AttriBox[MainStatusBar](Instance, )

  @staticmethod
  def link(url: Any) -> Callable:
    """Link to a URL."""
    if isinstance(url, str):
      url = QUrl(url)

    def go() -> bool:
      """Opens link in external browser."""
      return QDesktopServices.openUrl(url)

    return go

  def __init__(self, *args, **kwargs) -> None:
    """Initialize the BaseWindow."""
    self.__debug_flag__ = kwargs.get('_debug', None)
    QMainWindow.__init__(self, *args, **kwargs)
    self.setMouseTracking(True)

  def show(self) -> None:
    """Show the window."""
    if self.__is_initialized__ is None:  # Initialize the menu bar
      self.setMenuBar(self.mainMenuBar)
      self.setStatusBar(self.mainStatusBar)
      self.initUi()
      self._initCoreConnections()
      self.initSignalSlot()
      self.__is_initialized__ = True
    QMainWindow.show(self)

  def _initCoreConnections(self) -> None:
    """Initialize the core actions for the main window."""
    ic('Initializing core connections')
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #  Connecting File Menu Actions
    self.new = self.mainMenuBar.fileMenu.newAction
    self.open = self.mainMenuBar.fileMenu.openAction
    self.save = self.mainMenuBar.fileMenu.saveAction
    self.saveAs = self.mainMenuBar.fileMenu.saveAsAction
    self.preferences = self.mainMenuBar.fileMenu.prefAction
    self.exit = self.mainMenuBar.fileMenu.exitAction
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #  Connecting Edit Menu Actions
    self.selectAll = self.mainMenuBar.editMenu.selectAllAction
    self.copy = self.mainMenuBar.editMenu.copyAction
    self.cut = self.mainMenuBar.editMenu.cutAction
    self.paste = self.mainMenuBar.editMenu.pasteAction
    self.undo = self.mainMenuBar.editMenu.undoAction
    self.redo = self.mainMenuBar.editMenu.redoAction
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #  Connecting Help Menu Actions
    self.aboutQt = self.mainMenuBar.helpMenu.aboutQtAction
    self.aboutConda = self.mainMenuBar.helpMenu.aboutCondaAction
    self.aboutPython = self.mainMenuBar.helpMenu.aboutPythonAction
    self.aboutPySide6 = self.mainMenuBar.helpMenu.aboutPySide6Action
    self.help = self.mainMenuBar.helpMenu.helpAction
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #  Connecting Debug Menu Actions
    self.debug1 = self.mainMenuBar.debugMenu.debug01Action
    self.debug2 = self.mainMenuBar.debugMenu.debug02Action
    self.debug3 = self.mainMenuBar.debugMenu.debug03Action
    self.debug4 = self.mainMenuBar.debugMenu.debug04Action
    self.debug5 = self.mainMenuBar.debugMenu.debug05Action
    self.debug6 = self.mainMenuBar.debugMenu.debug06Action
    self.debug7 = self.mainMenuBar.debugMenu.debug07Action
    self.debug8 = self.mainMenuBar.debugMenu.debug08Action
    self.debug9 = self.mainMenuBar.debugMenu.debug09Action
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #  Connecting pulse signal
    self.pulse.connect(self.mainStatusBar.updateTime)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #  Connecting general signals
    self.exit.triggered.connect(self.requestQuit)
    self.exit.triggered.connect(self.close)
    self.help.triggered.connect(self.requestHelp)
    self.aboutQt.triggered.connect(QApplication.aboutQt)
    condaLink = self.link('https://conda.io')
    pythonLink = self.link('https://python.org')
    pysideLink = self.link('https://doc.qt.io/qtforpython/')
    helpLink = self.link('https://www.youtube.com/watch?v=l60MnDJklnM')
    self.aboutConda.triggered.connect(condaLink)
    self.aboutPython.triggered.connect(pythonLink)
    self.aboutPySide6.triggered.connect(pysideLink)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #  Connecting debug signals

  @Slot(str)
  def _announceHover(self, message) -> None:
    """Announce hover text."""
    self.statusBar().showMessage(message)

  @abstractmethod  # LayoutWindow
  def initUi(self, ) -> None:
    """Initializes the user interface for the main window."""

  @abstractmethod  # MainWindow
  def initSignalSlot(self, ) -> None:
    """Initializes the signal slot for the main window."""

  def showEvent(self, *args) -> None:
    """Show the window."""
    QMainWindow.showEvent(self, *args)
    self.statusBar().showMessage('Ready')

  def closeEvent(self, *args, **kwargs) -> None:
    """Close the window."""
    if self.__is_closing__:
      self.confirmQuit.emit()
      return QMainWindow.closeEvent(self, *args, **kwargs)
    self.__is_closing__ = True
    self.requestQuit.emit()
