"""EmptyBrush provides an empty instance of QBrush through the descriptor
protocol. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor


class EmptyBrush:
  """EmptyBrush provides an empty instance of QBrush through the descriptor
  protocol. """

  def __get__(self, instance: object, owner: type) -> Any:
    if instance is None:
      return self
    brush = QBrush()
    brush.setStyle(Qt.BrushStyle.NoBrush)
    brush.setColor(QColor(0, 0, 0, 0, ))
    return brush
