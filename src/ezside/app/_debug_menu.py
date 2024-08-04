"""DebugMenu provides a bunch of actions meant for use in debugging."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox, THIS
from icecream import ic

from ezside.app import EZAction, AbstractMenu

ic.configureOutput(includeContext=True)


class DebugMenu(AbstractMenu):
  """DebugMenu provides a bunch of actions meant for use in debugging."""

  debugAction02 = AttriBox[EZAction](THIS, 'Debug 02', 'F2', 'risitas.png')
  debugAction03 = AttriBox[EZAction](THIS, 'Debug 03', 'F3', 'risitas.png')
  debugAction04 = AttriBox[EZAction](THIS, 'Debug 04', 'F4', 'risitas.png')
  debugAction05 = AttriBox[EZAction](THIS, 'Debug 05', 'F5', 'risitas.png')
  debugAction06 = AttriBox[EZAction](THIS, 'Debug 06', 'F6', 'risitas.png')
  debugAction07 = AttriBox[EZAction](THIS, 'Debug 07', 'F7', 'risitas.png')
  debugAction08 = AttriBox[EZAction](THIS, 'Debug 08', 'F8', 'risitas.png')

  def initUi(self) -> None:
    """Initializes the menu"""
    self.addAction(self.debugAction02)
    self.addAction(self.debugAction03)
    self.addAction(self.debugAction04)
    self.addAction(self.debugAction05)
    self.addAction(self.debugAction06)
    self.addAction(self.debugAction07)
    self.addAction(self.debugAction08)
    self.__is_initialized__ = True

  def __init__(self, parent=None, *args) -> None:
    AbstractMenu.__init__(self, parent, 'Debug')
    self.initUi()
