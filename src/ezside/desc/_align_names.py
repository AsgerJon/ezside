"""The 'alignNames' module provides descriptor classes and parsers for
various core types in the PySide6 module."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt

AlignFlag = Qt.AlignmentFlag
AlignLeft = Qt.AlignmentFlag.AlignLeft
AlignRight = Qt.AlignmentFlag.AlignRight
AlignHCenter = Qt.AlignmentFlag.AlignHCenter
AlignTop = Qt.AlignmentFlag.AlignTop
AlignBottom = Qt.AlignmentFlag.AlignBottom
AlignVCenter = Qt.AlignmentFlag.AlignVCenter
AlignCenter = Qt.AlignmentFlag.AlignCenter

__all__ = [
  'AlignFlag', 'AlignLeft', 'AlignRight', 'AlignHCenter', 'AlignTop',
  'AlignBottom', 'AlignVCenter', 'AlignCenter'
]
