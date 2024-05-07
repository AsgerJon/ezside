"""MainStatusBar provides a status bar for the main application window."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ezside.app.menus import _AttriStatusBar


class MainStatusBar(_AttriStatusBar):
  """StatusBar provides a status bar for the main application window."""

  def initStyle(self, ) -> None:
    """Initialize the style of the menu. Subclasses may implement this
    method to customize the style of the menu. """

  def initUi(self, ) -> None:
    """Initializes the user interface for the status bar."""
    self.showMessage('Ready')
    self.setStyleSheet("""background-color: #e0e0e0; color: #000000;
    border-top: 1px solid #000000; border-left: 1px solid #000000;
    border-right: 1px solid #000000; border-bottom: 1px solid #000000;""")

  def initSignalSlot(self, ) -> None:
    """Initialize the signal-slot connections. Subclasses may implement this
    method, but generally the menu class is not responsible for handling
    actions just for presenting them. """
