"""CornerPanel provides corners together with horizontal and vertical
panels."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from vistutils.parse import maybe

from ezqt.core import Fixed
from ezqt.widgets import VerticalPanel


class CornerPanel(VerticalPanel):
  """CornerPanel provides corners together with horizontal and vertical
  panels."""

  def ___init__(self, size: int = None, *args, **kwargs) -> None:
    VerticalPanel.__init__(self, *args, **kwargs)
    size = maybe(size, 32)
    self.setFixedHeight(size)
    self.setFixedWidth(size)
    self.setSizePolicy(Fixed, Fixed)
