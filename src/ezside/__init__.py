"""The 'qol.app' module provides the graphical user interface based on the
pyside6 library."""
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from . import core
from . import app
from . import dialogs
from . import enums
from . import widgets

__all__ = [
    'app',
    'core',
    'dialogs',
    'enums',
    'widgets',
]
