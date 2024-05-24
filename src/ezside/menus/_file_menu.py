"""FileMenu subclasses CoreMenu and provides the file menu. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import QObject

from ezside.app import EZDesc
from ezside.menus import CoreMenu

Shiboken = type(QObject)
Menu = CoreMenu
if TYPE_CHECKING:
  pass
  from ezside.menus import CoreMenuBar

  Bar = CoreMenuBar


class FileMenu(CoreMenu):
  """FileMenu subclasses CoreMenu and provides the file menu. """

  def initUi(self, ) -> None:
    """Initialize the UI."""
    CoreMenu.initUi(self)
    self.setTitle('File')
    self.setTearOffEnabled(True)
    self.addAction('New')
    self.addAction('Open')
    self.addAction('Save')
    self.addAction('Save As')
    self.addSeparator()
    self.addAction('Exit')


class File(EZDesc):
  """File places the file menu in the menu bar using the descriptor
  protocol."""

  def getContentClass(self) -> type:
    """Returns the content class."""
    return FileMenu

  def create(self, instance: Bar, owner: type, **kwargs) -> FileMenu:
    """Create the content."""
    parent = instance.parent()
    kwargs['id'] = self.__settings_id__
    return FileMenu(parent, 'File', **kwargs, )
