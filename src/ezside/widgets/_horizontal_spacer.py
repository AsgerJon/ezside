"""HorizontalSpacer provides a widget that expands aggressively in the
horizontal direction, but only a few pixels in the horizontal direction.
When placed in a layout, it will pack other widgets tighter. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ezside.core import Expand, Tight
from ezside.widgets import BaseWidget


class HorizontalSpacer(BaseWidget):
  """HorizontalSpacer provides a widget that expands aggressively in the
  horizontal direction, but only a few pixels in the horizontal direction.
  When placed in a layout, it will pack other widgets tighter. """

  def initUi(self, ) -> None:
    """Initialize the user interface."""
    self.setSizePolicy(Expand, Tight, )
