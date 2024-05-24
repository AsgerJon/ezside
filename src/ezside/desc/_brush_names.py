"""The 'brushNames' module provides names for brush styles"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt

FillStyle = Qt.BrushStyle
SolidFill = Qt.BrushStyle.SolidPattern
NoFill = Qt.BrushStyle.NoBrush
HorFill = Qt.BrushStyle.HorPattern
VerFill = Qt.BrushStyle.VerPattern

__all__ = ['FillStyle', 'SolidFill', 'NoFill', 'HorFill', 'VerFill']
