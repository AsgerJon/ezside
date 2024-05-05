"""MainMenuBar subclasses QMenuBar and brings common menus with common
actions. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QMenuBar, QMenu
from attribox import AttriClass, AttriBox, this
from icecream import ic

from morevistutils.metadec import WhoDat

if TYPE_CHECKING:
  from ezside import BaseWindow
from ezside.app.menus import Menu

ic.configureOutput(includeContext=True, )


@WhoDat()
class MainMenuBar(QMenuBar, AttriClass):
  """MainMenuBar subclasses QMenuBar and brings common menus with common
  actions. """

  __main_menu_bar__ = True
  __main_window__ = None

  fileMenu = AttriBox[Menu]('File', this, )
  editMenu = AttriBox[Menu]('Edit', this, )
  helpMenu = AttriBox[Menu]('Help', this, )
  debugMenu = AttriBox[Menu]('Debug', this, )

  @staticmethod
  def getFileActions() -> list[str]:
    """Getter-function for file actions."""
    return ['new', 'open', 'save', 'save_as', '', 'exit']

  @staticmethod
  def getEditActions() -> list[str]:
    """Getter-function for edit actions."""
    return ['undo', 'redo', '', 'cut', 'copy', 'paste', '', 'select_all']

  @staticmethod
  def getHelpActions() -> list[str]:
    """Getter-function for help actions."""
    return ['aboutQt', 'aboutConda', 'aboutPython']

  @staticmethod
  def getDebugActions() -> list[str]:
    """Getter-function for debug actions."""
    return ['debug%d' % i for i in range(1, 10)]

  @classmethod
  def _getMenuDicts(cls) -> dict[str, list[str]]:
    """Getter-function for menu dictionaries."""
    return {
      'file' : cls.getFileActions(),
      'edit' : cls.getEditActions(),
      'help' : cls.getHelpActions(),
      'debug': cls.getDebugActions(),
    }

  @classmethod
  def getNamedMenuActions(cls, name: str) -> list[str]:
    """Getter-function for named menus."""
    return cls._getMenuDicts().get(name, [])

  def __init__(self, mainWindow: BaseWindow):
    """Initializes the menu bar."""
    self.__main_window__ = mainWindow
    QMenuBar.__init__(self)
    self.initUi()

  def initUi(self, ) -> None:
    """Initializes the user interface for the menu bar."""
    self.addMenu(self.fileMenu)
    self.addMenu(self.editMenu)
    self.addMenu(self.helpMenu)
    self.addMenu(self.debugMenu)

  def addMenu(self, *args, **kwargs) -> QMenu:
    """Reimplementation"""
    setattr(self, '__main_menu_bar__', True)
    return QMenuBar.addMenu(self, *args, **kwargs)

  def getMain(self) -> MainMenuBar:
    """Getter-function for the owning menu bar"""
    mainWindow = self.__main_window__
    if TYPE_CHECKING:
      assert isinstance(mainWindow, MainMenuBar)
    if mainWindow is not None:
      if getattr(mainWindow, '__main_window__', None) is not None:
        return mainWindow
      e = """Expected owning instance of MainMenuBar to have set the 
      attribute '__main_window__', but received: '%s' of type: '%s'"""
      raise AttributeError(e % (mainWindow, type(mainWindow)))
