"""MainWindow subclasses the LayoutWindow and provides the main
application business logic."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic

from ezside.windows import LayoutWindow

ic.configureOutput(includeContext=True, )


class MainWindow(LayoutWindow):
  """MainWindow subclasses the LayoutWindow and provides the main
  application business logic."""

  def initActions(self) -> None:
    """Initialize the actions."""
