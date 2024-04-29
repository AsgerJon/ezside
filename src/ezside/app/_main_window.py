"""MainWindow subclasses the LayoutWindow and provides the main
application business logic."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic

from ezside.app import LayoutWindow

ic.configureOutput(includeContext=True, )


class MainWindow(LayoutWindow):
  """MainWindow subclasses the LayoutWindow and provides the main
  application business logic."""

  def initActions(self) -> None:
    """Initialize the actions."""

  def testLineEditFunc(self, oldText: str, newText: str) -> None:
    """Test line edit function."""

  def testButtonFunc(self) -> None:
    """Test button function."""

  def testKeyFunc(self, key: str) -> None:
    """Test key function."""

  def testKeyNum(self, key: int) -> None:
    """Test key number."""

  def testKeyName(self, key: str) -> None:
    """Test key name."""
