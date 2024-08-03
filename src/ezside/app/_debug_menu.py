"""DebugMenu provides a bunch of actions meant for use in debugging."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox

from ezside.app import EZAction, AbstractMenu


class DebugMenu(AbstractMenu):
  """DebugMenu provides a bunch of actions meant for use in debugging."""

  debug02Action = AttriBox[EZAction]('Debug 02', 'F2', 'risitas.png')
  debug03Action = AttriBox[EZAction]('Debug 03', 'F3', 'risitas.png')
  debug04Action = AttriBox[EZAction]('Debug 04', 'F4', 'risitas.png')
  debug05Action = AttriBox[EZAction]('Debug 05', 'F5', 'risitas.png')
  debug06Action = AttriBox[EZAction]('Debug 06', 'F6', 'risitas.png')
  debug07Action = AttriBox[EZAction]('Debug 07', 'F7', 'risitas.png')
  debug08Action = AttriBox[EZAction]('Debug 08', 'F8', 'risitas.png')

  def initUi(self) -> None:
    """Initializes the menu"""
    self.addAction(self.debug02Action)
    self.addAction(self.debug03Action)
    self.addAction(self.debug04Action)
    self.addAction(self.debug05Action)
    self.addAction(self.debug06Action)
    self.addAction(self.debug07Action)
    self.addAction(self.debug08Action)

  def __init__(self, parent=None, *args) -> None:
    AbstractMenu.__init__(self, parent, 'Debug')
    self.initUi()
