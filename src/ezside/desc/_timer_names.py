"""The 'timerNames' module provides names for the Qt Enums for timers."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt

TimerType = Qt.TimerType
Precise = Qt.TimerType.PreciseTimer
Coarse = Qt.TimerType.CoarseTimer
VeryCoarse = Qt.TimerType.VeryCoarseTimer

__all__ = ['TimerType', 'Precise', 'Coarse', 'VeryCoarse']
