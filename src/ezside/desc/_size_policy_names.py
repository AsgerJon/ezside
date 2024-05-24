"""The 'sizePolicyNames' module provides names for the Qt Enums for size
policies."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QSizePolicy

Policy = QSizePolicy.Policy
Fixed = QSizePolicy.Policy.Fixed
Prefer = QSizePolicy.Policy.Preferred
Expand = QSizePolicy.Policy.MinimumExpanding
Tight = QSizePolicy.Policy.Maximum

__all__ = ['Policy', 'Fixed', 'Prefer', 'Expand', 'Tight']
