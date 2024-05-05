"""BaseWindow provides the base class for the main application window. It
implements menus and actions for the application, leaving widgets for the
LayoutWindow class."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Signal, QCoreApplication
from PySide6.QtWidgets import QMainWindow
from attribox import AttriBox, this, AttriClass
from icecream import ic

from ezside.app.menus import MainMenuBar, MainStatusBar

ic.configureOutput(includeContext=True, )


class BaseWindow(QMainWindow, AttriClass):
  """BaseWindow class provides menus and actions for the application."""

  __main_window__ = True

  __is_initialized__ = None
  __running_app__ = None

  mainMenuBar = AttriBox[MainMenuBar](this)
  mainStatusBar = AttriBox[MainStatusBar](this)

  requestQuit = Signal()
  requestHelp = Signal()

  def getApp(self) -> QCoreApplication:
    """Getter-function for running application"""
    return self.__running_app__

  def show(self) -> None:
    """Show the window."""
    if self.__is_initialized__ is None:
      self.initMenus()
      self.initStyle()
      self.initUi()

      self.initSignalSlot()
      self.__is_initialized__ = True
    QMainWindow.show(self)

  def initMenus(self, ) -> None:
    """Initializes the user interface for the main window."""
    # self.mainMenuBar.debug.debug1.triggered.connect(self.debug1Func)
    # self.mainMenuBar.debug.debug2.triggered.connect(self.debug2Func)
    # self.mainMenuBar.debug.debug3.triggered.connect(self.debug3Func)
    # self.mainMenuBar.debug.debug4.triggered.connect(self.debug4Func)
    # self.mainMenuBar.debug.debug5.triggered.connect(self.debug5Func)
    # self.mainMenuBar.debug.debug6.triggered.connect(self.debug6Func)
    # self.mainMenuBar.debug.debug7.triggered.connect(self.debug7Func)
    # self.mainMenuBar.debug.debug8.triggered.connect(self.debug8Func)
    # self.mainMenuBar.debug.debug9.triggered.connect(self.debug9Func)
    self.mainMenuBar.fileMenu.connectAction('new', self.newFunc)
    self.mainMenuBar.fileMenu.connectAction('open', self.openFunc)
    self.mainMenuBar.fileMenu.connectAction('save', self.saveFunc)
    self.mainMenuBar.fileMenu.connectAction('saveAs', self.saveAsFunc)
    self.mainMenuBar.fileMenu.connectAction('exit', self.exitFunc)
    self.setMenuBar(self.mainMenuBar)
    self.mainStatusBar.initUi()
    self.setStatusBar(self.mainStatusBar)

  def newFunc(self, ) -> None:
    """New function."""
    note = 'New function called'
    print(note)
    self.statusBar().showMessage(note)

  def openFunc(self, ) -> None:
    """Open function."""
    note = 'Open function called'
    print(note)
    self.statusBar().showMessage(note)

  def saveFunc(self, ) -> None:
    """Save function."""
    note = 'Save function called'
    print(note)
    self.statusBar().showMessage(note)

  def saveAsFunc(self, ) -> None:
    """Save as function."""
    note = 'Save as function called'
    print(note)
    self.statusBar().showMessage(note)

  def exitFunc(self, ) -> None:
    """Exit function."""
    note = 'Exit function called'
    print(note)
    self.statusBar().showMessage(note)

  def initStyle(self, ) -> None:
    """Initializes the style of the main window."""

  def initUi(self, ) -> None:
    """Initializes the user interface for the main window."""

  def initSignalSlot(self, ) -> None:
    """Initializes the signal slot for the main window."""

  def debug1Func(self, ) -> None:
    """Debug1 function."""
    note = 'Debug1 function called'
    print(note)
    self.statusBar().showMessage(note)

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
