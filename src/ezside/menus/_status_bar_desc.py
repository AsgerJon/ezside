"""StatusBar provides the status bar through the descriptor protocol."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ezside.app import EZDesc
from ezside.menus import CoreStatusBar

if TYPE_CHECKING:
  from ezside.windows import CoreWindow as Win

Bar = CoreStatusBar


class StatusBarInstance(Bar):
  """StatusBar provides the status bar through the descriptor protocol."""

  def initUi(self) -> None:
    """Initializes the user interface."""
    self.showMessage('Ready')


class StatusBar(EZDesc):
  """StatusBarDesc provides the descriptor for the StatusBar class."""

  __parent_widget__ = None

  def getContentClass(self) -> type:
    """Returns the content class."""
    return Bar

  def create(self, instance: Win, owner: type, **kwargs) -> Bar:
    """Create the content."""
    parent = instance.parent()
    return StatusBarInstance(parent, 'StatusBar', id='statusBar')
