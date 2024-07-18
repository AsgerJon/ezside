"""MainMenuBar subclasses QMenuBar and brings common menus with common
actions. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenuBar, QMenu
from icecream import ic
from worktoy.desc import AttriBox

from ezside.app.menus import FileMenu, EditMenu, HelpMenu, \
  DebugMenu, AbstractMenu

if TYPE_CHECKING:
  pass
ic.configureOutput(includeContext=True, )


class MainMenuBar(QMenuBar):
  """MainMenuBar subclasses QMenuBar and brings common menus with common
  actions. """

  __iter_contents__ = None
  __added_menus__ = None

  fileMenu = AttriBox[FileMenu]()
  editMenu = AttriBox[EditMenu]()
  helpMenu = AttriBox[HelpMenu]()
  debugMenu = AttriBox[DebugMenu]()

  hoverText = Signal(str)

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the MainMenuBar."""
    QMenuBar.__init__(self, *args, **kwargs)
    self.initUi()
    self.initSignalSlot()

  def initUi(self, ) -> None:
    """Initializes the user interface for the widget. Required for subclasses
    to implement. """
    self.fileMenu.initUi()
    self.addMenu(self.fileMenu)
    self.editMenu.initUi()
    self.addMenu(self.editMenu)
    self.helpMenu.initUi()
    self.addMenu(self.helpMenu)
    self.debugMenu.initUi()
    self.addMenu(self.debugMenu)

  def initSignalSlot(self) -> None:
    """Initializes the signal/slot connections for the widget. Optional for
    subclasses to implement."""

  def _getMenuList(self) -> list[AbstractMenu]:
    """Return a list of menus."""
    if self.__added_menus__ is None:
      self.__added_menus__ = []
    return self.__added_menus__

  def addMenu(self, *args) -> QAction:
    """Add a menu to the menu bar. """
    for arg in args:
      if isinstance(arg, AbstractMenu):
        existing = self._getMenuList()
        self.__added_menus__ = [*existing, arg]
        return super().addMenu(arg)
    else:
      return QMenuBar.addMenu(self, *args)

  def __iter__(self) -> MainMenuBar:
    """Iterate over the contents of the menu bar."""
    self.__iter_contents__ = self._getMenuList()
    return self

  def __next__(self, ) -> AbstractMenu:
    """Implementation of iteration protocol"""
    if self.__iter_contents__:
      return self.__iter_contents__.pop(0)
    raise StopIteration

  def __len__(self) -> int:
    """Return the number of menus in the menu bar."""
    return len(self.__added_menus__)

  def __contains__(self, other: QMenu) -> bool:
    """Check if a menu is in the menu bar."""
    for menu in self:
      if menu is other:
        return True
    else:
      return False
