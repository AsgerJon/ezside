"""CoreMenu provides the menu entry point for menus inheriting from both
QMenu and EZObject. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QMenu

from ezside.app import EZObject
from ezside.core import parseParent


class CoreMenu(QMenu, EZObject):
  """CoreMenu provides the menu entry point for menus inheriting from both
  QMenu and EZObject. """

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the CoreMenu."""
    parent = parseParent(*args, **kwargs)
    QMenu.__init__(self, parent)
    EZObject.__init__(self, *args, **kwargs)
