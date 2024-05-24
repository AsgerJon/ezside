"""EditMenu subclasses AbstractMenu and brings common edit actions:
  - Undo
  - Redo
  - Cut
  - Copy
  - Paste
  - Delete
  - Select All
"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import QObject

from ezside.app import EZDesc
from ezside.menus import CoreMenu

if TYPE_CHECKING:
  from ezside.menus import CoreMenuBar

  Bar = CoreMenuBar

Shiboken = type(QObject)


class EditMenu(CoreMenu):
  """EditMenu subclasses CoreMenu and provides the edit menu. """

  def initUi(self, ) -> None:
    """Initialize the UI."""
    CoreMenu.initUi(self)
    self.setTitle('Edit')
    self.setTearOffEnabled(False)
    self.addAction('Undo')
    self.addAction('Redo')
    self.addSeparator()
    self.addAction('Cut')
    self.addAction('Copy')
    self.addAction('Paste')
    self.addSeparator()
    self.addAction('Select All')


class Edit(EZDesc):
  """Edit places the edit menu in the menu bar using the descriptor
  protocol."""

  def getContentClass(self) -> type:
    """Returns the content class."""
    return EditMenu

  def create(self, instance: Bar, owner: type, **kwargs) -> EditMenu:
    """Create the content."""
    parent = instance.parent()
    return EditMenu(parent, 'Edit', id='mainMenu')
