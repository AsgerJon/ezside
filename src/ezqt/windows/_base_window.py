"""BaseWindow provides the base class for the main application window. It
implements menus and actions for the application, leaving widgets for the
LayoutWindow class."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QMainWindow

from attribox import AttriBox, this
from ezqt.windows.bars import MenuBar, StatusBar

setattr(type(QMainWindow), '__str__', lambda cls: cls.__qualname__)
setattr(type(QMainWindow), '__repr__', lambda cls: cls.__qualname__)


class BaseWindow(QMainWindow):
  """BaseWindow provides the base class for the main application window. It
  implements menus and actions for the application, leaving widgets for the
  LayoutWindow class."""

  mainMenuBar = AttriBox[MenuBar](this)
  mainStatusBar = AttriBox[StatusBar](this)

  def initUi(self, ) -> None:
    """Initializes the user interface for the main window."""
    self.mainMenuBar.initUi()
    self.setMenuBar(self.mainMenuBar)
    self.mainStatusBar.initUi()
    self.setStatusBar(self.mainStatusBar)

  def connectActions(self) -> None:
    """Connects the actions to the business logic."""
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