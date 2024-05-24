"""HelpMenu subclasses CoreMenu and provides the help menu:

  - About Qt
  - About PySide6
  - About Python
  - About Conda
"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import QObject

from ezside.app import EZDesc
from ezside.menus import CoreMenu

Shiboken = type(QObject)

if TYPE_CHECKING:
  from ezside.menus import CoreMenuBar as Bar


class HelpMenu(CoreMenu):
  """HelpMenu subclasses CoreMenu and provides the help menu. """

  def initUi(self, ) -> None:
    """Initialize the UI."""
    CoreMenu.initUi(self)
    self.setTitle('Help')
    self.setTearOffEnabled(True)
    self.addAction('About Qt')
    self.addAction('About PySide6')
    self.addAction('About Python')
    self.addAction('About Conda')


class Help(EZDesc):
  """Help places the help menu in the menu bar using hte descriptor
  protocol."""

  def getContentClass(self) -> type:
    """Returns the content class."""
    return HelpMenu

  def create(self, instance: Bar, owner: type, **kwargs) -> HelpMenu:
    """Create the content."""
    parent = instance.parent()
    return HelpMenu(parent, 'Help', id='mainMenu')
