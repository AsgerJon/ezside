"""DebugMenu provides debugging actions."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ezside.app import EZDesc
from ezside.menus import CoreMenu

if TYPE_CHECKING:
  from ezside.menus import CoreMenuBar as Bar


class DebugMenu(CoreMenu):
  """DebugMenu provides debugging actions."""

  def initUi(self, ) -> None:
    """Initializes the user interface."""
    CoreMenu.initUi(self)
    self.setTitle("Debug")
    self.setTearOffEnabled(False)
    self.addAction('Debug01')
    self.addAction('Debug02')
    self.addAction('Debug03')
    self.addAction('Debug04')
    self.addAction('Debug05')
    self.addAction('Debug06')
    self.addAction('Debug07')
    self.addAction('Debug08')
    self.addAction('Debug09')


class Debug(EZDesc):
  """Debug places the debug menu in the menu bar using the descriptor
  protocol."""

  def getContentClass(self) -> type:
    """Returns the content class."""
    return DebugMenu

  def create(self, instance: Bar, owner: type, **kwargs) -> DebugMenu:
    """Create the content."""
    parent = instance.parent()
    return DebugMenu(parent, 'Debug', id='mainMenu')
