"""MenuBar provides the menu bar for the main application window."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from PySide6.QtWidgets import QMenuBar
from attribox import AttriBox, this, AttriClass
from icecream import ic
from vistutils.text import monoSpace

from ezside.app.menus import FilesMenu, EditMenu, HelpMenu, DebugMenu

if TYPE_CHECKING:
  from ezside import BaseWindow

ic.configureOutput(includeContext=True, )


class MainMenuBar(QMenuBar, AttriClass):
  """MenuBar provides the menu bar for the main application window."""

  __main_menu_bar__ = True

  files = AttriBox[FilesMenu](this)
  edit = AttriBox[EditMenu](this)
  help = AttriBox[HelpMenu](this)
  debug = AttriBox[DebugMenu](this)

  def getMain(self) -> Any:  # MainWindow
    """Returns the main window."""
    mainWindow = self.getOwningInstance()
    if getattr(mainWindow, '__main_window__', None) is not None:
      return mainWindow
    e = """Expected owning instance of MainMenuBar to have set the 
    attribute '__main_window__', but received: '%s' of type: '%s'"""
    insName = '%s' % mainWindow
    clsName = mainWindow.__class__.__name__
    raise AttributeError(monoSpace(e % (insName, clsName)))

  def getApp(self, ) -> Any:  # App
    """Returns the running application."""
    mainWindow = self.getMain()
    if isinstance(mainWindow, AttriClass):
      return mainWindow.getOwningInstance()

  def initStyle(self) -> None:
    """Initialize the style of the widget"""

  def initUi(self, ) -> None:
    """Initializes the user interface for the menu bar."""
    self.addMenu(self.files)
    self.addMenu(self.edit)
    self.addMenu(self.help)
    self.addMenu(self.debug)

  def initSignalSlot(self) -> None:
    """Initialize the signal slot"""

  def setOnWindow(self, window: BaseWindow) -> None:
    """Sets the menu bar on the window."""
    self.initStyle()
    self.initUi()
    self.initSignalSlot()
    window.setMenuBar(self)
