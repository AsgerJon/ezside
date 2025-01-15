"""AbstractAction subclasses QAction implementing specific type overloads."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget


class AbstractAction(QAction):
  """AbstractAction subclasses QAction implementing specific type
  overloads."""

  def __init__(self, parent: QWidget, title: str, shortCut: str) -> None:
    """Initialize the AbstractAction."""
    QAction.__init__(self, title, parent)
    self.setShortcut(shortCut)
