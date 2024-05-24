"""MenuBarDesc provides exposes the MenuBar class through the descriptor
protocol."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QMenu

from ezside.app import EZDesc
from ezside.menus import CoreMenuBar, Help, Edit, File, Debug
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from ezside.windows import CoreWindow as Win

Bar = CoreMenuBar


class MenuBarInstance(Bar):
  """MenuBar class provides the main menu bar for the main application."""

  file = File(id='mainMenu')
  edit = Edit(id='mainMenu')
  help = Help(id='mainMenu')
  debug = Debug(id='mainMenu')

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the MenuBar."""
    CoreMenuBar.__init__(self, *args, **kwargs)

  def initUi(self) -> None:
    """Initializes the user interface."""
    self.file.initUi()
    QMenu.setTearOffEnabled(self.file, False)
    self.addMenu(self.file)
    self.edit.initUi()
    QMenu.setTearOffEnabled(self.edit, False)
    self.addMenu(self.edit)
    self.help.initUi()
    QMenu.setTearOffEnabled(self.help, False)
    self.addMenu(self.help)
    self.debug.initUi()
    QMenu.setTearOffEnabled(self.debug, False)
    self.addMenu(self.debug)


class MenuBar(EZDesc):
  """MenuBarDesc class provides the descriptor for the MenuBar class."""

  def getContentClass(self) -> type:
    """Returns the content class."""
    return Bar

  def create(self, instance: Win, owner: type, **kwargs) -> Bar:
    """Create the content."""
    parent = instance.parent()
    return MenuBarInstance(parent, 'MenuBar', id='mainMenu')
