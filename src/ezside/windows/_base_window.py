"""BaseWindow provides the base class for the main application window. It
implements menus and actions for the application, leaving widgets for the
LayoutWindow class."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QMainWindow
from attribox import AttriBox, this
from icecream import ic

from ezside.windows.bars import MenuBar, StatusBar

ic.configureOutput(includeContext=True, )


class BaseWindow(QMainWindow):
  """BaseWindow provides the base class for the main application window. It
  implements menus and actions for the application, leaving widgets for the
  LayoutWindow class."""

  def __init__(self, ) -> None:
    QMainWindow.__init__(self)
    self.mainMenuBar = None
    self.mainStatusBar = None

  # mainMenuBar = AttriBox[MenuBar](this)
  # mainStatusBar = AttriBox[StatusBar](this)
  #
  # def initMenus(self, ) -> None:
  #   """Initializes the user interface for the main window."""
  #   ic('initMenus')
  #   self.menuBar().clear()
  #   self.mainMenuBar.initUi()
  #   self.setMenuBar(self.mainMenuBar)
  #   self.mainStatusBar.initUi()
  #   self.setStatusBar(self.mainStatusBar)
  #
  # def debug1Func(self, ) -> None:
  #   """Debug1 function."""
  #   note = 'Debug1 function called'
  #   print(note)
  #   self.statusBar().showMessage(note)
  #
  # def debug2Func(self, ) -> None:
  #   """Debug2 function."""
  #   note = 'Debug2 function called'
  #   print(note)
  #   self.statusBar().showMessage(note)
  #
  # def debug3Func(self, ) -> None:
  #   """Debug3 function."""
  #   note = 'Debug3 function called'
  #   print(note)
  #   self.statusBar().showMessage(note)
  #
  # def debug4Func(self, ) -> None:
  #   """Debug4 function."""
  #   note = 'Debug4 function called'
  #   print(note)
  #   self.statusBar().showMessage(note)
  #
  # def debug5Func(self, ) -> None:
  #   """Debug5 function."""
  #   note = 'Debug5 function called'
  #   print(note)
  #   self.statusBar().showMessage(note)
  #
  # def debug6Func(self, ) -> None:
  #   """Debug6 function."""
  #   note = 'Debug6 function called'
  #   print(note)
  #   self.statusBar().showMessage(note)
  #
  # def debug7Func(self, ) -> None:
  #   """Debug7 function."""
  #   note = 'Debug7 function called'
  #   print(note)
  #   self.statusBar().showMessage(note)
  #
  # def debug8Func(self, ) -> None:
  #   """Debug8 function."""
  #   note = 'Debug8 function called'
  #   print(note)
  #   self.statusBar().showMessage(note)
  #
  # def debug9Func(self, ) -> None:
  #   """Debug9 function."""
  #   note = 'Debug9 function called'
  #   print(note)
  #   self.statusBar().showMessage(note)
