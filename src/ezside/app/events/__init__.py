"""The 'qol.app.events' module provides the event classes used by the
application."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ._mouse_event import MouseEvent
from ._mouse_release import MouseRelease
from ._compound_click import CompoundClick

__all__ = [
    'MouseEvent',
    'MouseRelease',
    'CompoundClick',
]
