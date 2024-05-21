"""CoreWidget provides the widget entry point by inheriting from both
QWidget and EZObject."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QWidget
from icecream import ic

from ezside.app import EZObject
from ezside.core import parseParent

if TYPE_CHECKING:
  pass

ic.configureOutput(includeContext=True)


class CoreWidget(QWidget, EZObject):
  """CoreWidget provides the widget entry point by inheriting from both
  QWidget and EZObject."""

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the CoreWidget."""
    parent = parseParent(*args, **kwargs)
    QWidget.__init__(self, parent)
    EZObject.__init__(self, *args, **kwargs)
