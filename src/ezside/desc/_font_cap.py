"""The 'fontCap' module names the Qt Enums for font capitalization."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QFont

FontCap = QFont.Capitalization
MixedCap = QFont.Capitalization.MixedCase
AllCap = QFont.Capitalization.AllUppercase
SmallCap = QFont.Capitalization.SmallCaps
LowCap = QFont.Capitalization.AllLowercase

__all__ = ['FontCap', 'MixedCap', 'AllCap', 'SmallCap', 'LowCap']
