"""ClockWidget provides a widget for displaying the current time. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ezside.widgets import BaseWidget


class ClockWidget(BaseWidget):
  """ClockWidget provides a widget for displaying the current time. """

  __seven_seg__ = None

  def initUi(self) -> None:
    """Initialize the user interface."""
