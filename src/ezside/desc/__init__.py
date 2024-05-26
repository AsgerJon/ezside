"""The 'desc' module provides descriptor classes and parsers for various
core types in the PySide6 module."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ._brush_names import *
from ._pen_names import *
from ._colour_names import *
from ._align_names import *
from ._orientation_names import *
from ._size_policy_names import *
from ._timer_names import *
from ._font_weight import *
from ._font_cap import *
from ._font_families import *
from ._dialog_names import *
from ._ez_timer import EZTimer
from ._fit_text import fitText
from ._settings_descriptor import SettingsDescriptor
from ._point_descriptor import Point, parsePoint
from ._margin_descriptor import Margins, parseMargins
from ._parse_parent import parseParent
from ._parse_filter import parseFilter
from ._parse_window import parseWindow
from ._parse_colour import parseColour, parseColor
from ._brush import Brush, emptyBrush, parseBrush
from ._alignment import VAlign, HAlign, parseAlignFlag
from ._font import Font, parseFont
from ._pen import Pen, emptyPen, parsePen
