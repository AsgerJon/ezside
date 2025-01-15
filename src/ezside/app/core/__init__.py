"""The 'qol.app.core' module provides core dataclasses shared by the
application."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ._empty_pen import EmptyPen
from ._empty_brush import EmptyBrush
from ._point import Point
from ._vector2d import Vector2D
from ._size import Size
from ._margin import Margin
from ._rgba import RGBA
from ._box_model import BoxModel
from ._rect import Rect

from ._font_family import FontFamily
from ._font import Font

from ._text_model import TextModel

__all__ = [
    'EmptyPen',
    'EmptyBrush',
    'Margin',
    'BoxModel',
    'RGBA',
    'Point',
    'Vector2D',
    'Size',
    'Rect',
    'FontFamily',
    'Font',
    'TextModel',
]
