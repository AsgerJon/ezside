"""CoreDialog provides the entry point for dialogs inheriting from both
QDialog and EZObject. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QDialog

from ezside.app import EZObject
from ezside.desc import parseParent


class CoreDialog(QDialog, EZObject):
  """CoreDialog provides the entry point for dialogs inheriting from both
  QDialog and EZObject. """

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the CoreDialog."""
    parent = parseParent(*args, **kwargs)
    QDialog.__init__(self, parent)
    EZObject.__init__(self, *args, **kwargs)
