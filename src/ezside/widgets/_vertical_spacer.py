"""VerticalSpacer provides a widget that expands aggressively in the vertical
direction, but only a few pixels in the horizontal direction. When placed
in a layout, it will pack other widgets tighter. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ezside.core import Tight, Expand
from ezside.widgets import BaseWidget
from typing import Any


class VerticalSpacer(BaseWidget):
  """VerticalSpacer provides a widget that expands aggressively in the
  vertical direction, but only a few pixels in the horizontal direction.
  When placed in a layout, it will pack other widgets tighter. """

  @classmethod
  def registerFields(cls) -> dict[str, Any]:
    """Registers field"""
    return {}

  @classmethod
  def registerStates(cls) -> list[str]:
    """Registers states"""
    return ['base', ]

  @classmethod
  def registerDynamicFields(cls) -> dict[str, Any]:
    """Registers dynamic fields"""
    return {}

  def detectState(self) -> str:
    """State detection"""
    return 'base'

  def initUi(self, ) -> None:
    """Initialize the user interface."""
    self.setSizePolicy(Tight, Expand, )
