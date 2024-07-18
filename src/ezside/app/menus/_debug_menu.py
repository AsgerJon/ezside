"""DebugMenu provides a debug menu for the main application window. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox, Instance

from ezside.app.menus import AbstractMenu, Action


class DebugMenu(AbstractMenu):
  """DebugMenu provides a debug menu for the main application window. """

  debug01Action = AttriBox[Action](Instance, 'Debug01', icon='risitas')
  debug02Action = AttriBox[Action](Instance, 'Debug02', icon='risitas')
  debug03Action = AttriBox[Action](Instance, 'Debug03', icon='risitas')
  debug04Action = AttriBox[Action](Instance, 'Debug04', icon='risitas')
  debug05Action = AttriBox[Action](Instance, 'Debug05', icon='risitas')
  debug06Action = AttriBox[Action](Instance, 'Debug06', icon='risitas')
  debug07Action = AttriBox[Action](Instance, 'Debug07', icon='risitas')
  debug08Action = AttriBox[Action](Instance, 'Debug08', icon='risitas')
  debug09Action = AttriBox[Action](Instance, 'Debug09', icon='risitas')

  def initUi(self) -> None:
    """Initialize the user interface."""
    self.addAction(self.debug01Action)
    self.addAction(self.debug02Action)
    self.addAction(self.debug03Action)
    self.addAction(self.debug04Action)
    self.addAction(self.debug05Action)
    self.addAction(self.debug06Action)
    self.addAction(self.debug07Action)
    self.addAction(self.debug08Action)
    self.addAction(self.debug09Action)
