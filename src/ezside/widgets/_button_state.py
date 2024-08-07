"""ButtonState enumerates the different states of a button using the
KeeNum class from the 'worktoy.keenum' module. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import Field
from worktoy.keenum import KeeNum, auto


class ButtonState(KeeNum):
  """ButtonState enumerates the different states of a button."""

  active = Field()
  hover = Field()
  pressed = Field()

  DISABLED_HOVER = auto()
  DISABLED_RELEASED = auto()
  DISABLED_PRESSED = auto()
  ENABLED_HOVER = auto()
  ENABLED_RELEASED = auto()
  ENABLED_PRESSED = auto()

  @active.GET
  def _getActive(self) -> bool:
    """Getter-function for enumerations that represent enabled."""
    return True if 'enabled' in self.name.lower() else False

  @hover.GET
  def _getHover(self) -> bool:
    """Getter-function for enumerations that represent hover."""
    return True if 'hover' in self.name.lower() else False

  @pressed.GET
  def _getPressed(self) -> bool:
    """Getter-function for enumerations that represent pressed."""
    return True if 'pressed' in self.name.lower() else False

  def __int__(self) -> int:
    out = 1
    if self.active:
      out *= 2
    if self.hover:
      out *= 3
    if self.pressed:
      out *= 5
    return out

  def __hash__(self, ) -> int:
    return int(self)
