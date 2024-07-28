"""MenuBar subclasses QMenuBar and provides a menu bar for the main
window."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QMenuBar
from worktoy.desc import AttriBox, THIS

from ezside.app import FileMenu


class MenuBar(QMenuBar):
  """MenuBar subclasses QMenuBar and provides a menu bar for the main
  window."""

  fileMenu = AttriBox[FileMenu](THIS, 'File')

  def __init__(self, *args) -> None:
    """Initializes the object"""
    QMenuBar.__init__(self)
