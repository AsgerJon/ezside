"""The 'qol.app.enums' module provides the enumerations used by the
application."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ._abstract_enum import AbstractEnum
from ._horizontal_align import HorizontalAlign
from ._vertical_align import VerticalAlign
from ._align import Align
from ._base_size_policy import BaseSizePolicy
from ._size_policy import SizePolicy
from ._mouse_button import MouseButton
from ._mouse_event_type import MouseEventType
from ._key_mod import KeyMod

__all__ = [
    'AbstractEnum',
    'HorizontalAlign',
    'VerticalAlign',
    'Align',
    'BaseSizePolicy',
    'MouseButton',
    'MouseEventType',
    'KeyMod',
]
