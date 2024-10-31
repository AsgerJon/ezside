"""Drawing provides a widget providing a visual representation of a
collection of points and connections. As a CAD tool, it combines this with
user interaction. It is effectively both input and output for the user."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ezside.layouts import BoxWidget
from ezside.style import BoxStyle


class Drawing(BoxWidget):
  """Drawing provides a widget providing a visual representation of a
  collection of points and connections. As a CAD tool, it combines this with
  user interaction. It is effectively both input and output for the user."""

  def initSignalSlot(self) -> None:
    """Initialize the signal-slot connections."""

  def __init__(self, *args, **kwargs) -> None:
    BoxWidget.__init__(self, *args, **kwargs)
    self.setMouseTracking(True)
    self.initSignalSlot()

  def _getBoxStyle(self) -> BoxStyle:
    """Reimplementation of BoxStyle fitting the Drawing widget."""
    raise NotImplementedError
