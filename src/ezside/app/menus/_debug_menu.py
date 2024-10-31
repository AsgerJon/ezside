"""DebugMenu provides a bunch of actions meant for use in debugging."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox, THIS
from icecream import ic

from ezside.app.menus import EZAction, EZMenu

ic.configureOutput(includeContext=True)


class DebugMenu(EZMenu):
  """DebugMenu provides a bunch of actions meant for use in debugging."""

  debugAction02 = AttriBox[EZAction](THIS, 'Debug 02', 'F2', )
  debugAction03 = AttriBox[EZAction](THIS, 'Debug 03', 'F3', )
  debugAction04 = AttriBox[EZAction](THIS, 'Debug 04', 'F4', )
  debugAction05 = AttriBox[EZAction](THIS, 'Debug 05', 'F5', )
  debugAction06 = AttriBox[EZAction](THIS, 'Debug 06', 'F6', )
  debugAction07 = AttriBox[EZAction](THIS, 'Debug 07', 'F7', )
  debugAction08 = AttriBox[EZAction](THIS, 'Debug 08', 'F8', )

  def initMenu(self) -> None:
    """Initializes the menu"""
    self.addAction(self.debugAction02)
    self.addAction(self.debugAction03)
    self.addAction(self.debugAction04)
    self.addAction(self.debugAction05)
    self.addAction(self.debugAction06)
    self.addAction(self.debugAction07)
    self.addAction(self.debugAction08)
