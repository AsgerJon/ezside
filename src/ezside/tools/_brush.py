"""This file provides functions relating to QBrush instances."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor


def emptyBrush() -> QBrush:
  """Return a QBrush with no color."""
  brush = QBrush()
  brush.setStyle(Qt.BrushStyle.NoBrush)
  brush.setColor(QColor(0, 0, 0, 0, ))
  return brush


def fillBrush(color: QColor) -> QBrush:
  """Return a QBrush filled with the specified color."""
  brush = QBrush()
  brush.setStyle(Qt.BrushStyle.SolidPattern)
  brush.setColor(color)
  return brush
