"""The 'penNames' module provides names for QPen styles and cap styles."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt

LineStyle = Qt.PenStyle
SolidLine = Qt.PenStyle.SolidLine
DashLine = Qt.PenStyle.DashLine
DotLine = Qt.PenStyle.DotLine
DashDotLine = Qt.PenStyle.DashDotLine
DashDotDotLine = Qt.PenStyle.DashDotDotLine
NoPen = Qt.PenStyle.NoPen
CapStyle = Qt.PenCapStyle
FlatCap = Qt.PenCapStyle.FlatCap
SquareCap = Qt.PenCapStyle.SquareCap
RoundCap = Qt.PenCapStyle.RoundCap
JoinStyle = Qt.PenJoinStyle
RoundPen = Qt.PenJoinStyle.RoundJoin
BevelPen = Qt.PenJoinStyle.BevelJoin
MiterPen = Qt.PenJoinStyle.MiterJoin

__all__ = [
  'LineStyle', 'SolidLine', 'DashLine', 'DotLine', 'DashDotLine',
  'DashDotDotLine', 'NoPen', 'CapStyle', 'FlatCap', 'SquareCap',
  'RoundCap', 'JoinStyle', 'RoundPen', 'BevelPen', 'MiterPen'
]
