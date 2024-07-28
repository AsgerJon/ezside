"""This subclass should implement business logic."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ezside.app import LayoutWindow


class MainWindow(LayoutWindow):
  """This subclass should implement business logic."""

  def initSignalSlot(self) -> None:
    """Initialize signals and slots."""
    self.debugAction01.triggered.connect(self.debugSlot01)

  def show(self) -> None:
    """Reimplementation setting up signals and slots before invoking
    parent method."""
    self.initSignalSlot()
    LayoutWindow.show(self)

  def debugSlot01(self) -> None:
    """Debug slot 01"""
    self.welcomeLabel.text += '.'
