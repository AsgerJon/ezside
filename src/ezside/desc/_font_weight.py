"""The 'fontWeight' module provides names font weights Enum. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QFont

Weight = QFont.Weight
Thin = QFont.Weight.Thin
Light = QFont.Weight.Light
Normal = QFont.Weight.Normal
Medium = QFont.Weight.Medium
Bold = QFont.Weight.Bold

fontWeights = {
  'Thin'  : Thin,
  'Light' : Light,
  'Normal': Normal,
  'Medium': Medium,
  'Bold'  : Bold
}

__all__ = ['fontWeights', 'Weight', 'Thin', 'Light', 'Normal', 'Medium',
           'Bold']
