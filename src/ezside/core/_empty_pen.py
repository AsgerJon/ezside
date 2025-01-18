"""EmptyPen provides an empty instance of QPen through the descriptor
protocol. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtGui import QPen


class EmptyPen:
  """EmptyPen provides an empty instance of QPen through the descriptor
  protocol. """

  def __get__(self, instance: object, owner: type) -> Any:
    if instance is None:
      return self
    pen = QPen()
    pen.setStyle(Qt.PenStyle.NoPen)
    return pen
