"""The 'ezside.tools' module provides functions streamlining the creation
of instances of QFont, QPen, QBrush and similar. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ._color_box import ColorBox
from ._align import Align
from ._font_cap import FontCap
from ._font_family import FontFamily
from ._font_flag import FontFlag, Italic, StrikeOut, Underline
from ._font_weight import FontWeight
from ._font import Font
from ._abstract_style import AbstractStyle
from ._box_style import BoxStyle
from ._font_style import FontStyle

from ._control_data import ControlData
from ._mouse_timer import MouseTimer
from ._button_state import ButtonState
from ._margins_box import MarginsBox
from ._timer import Timer
from ._load_resource import LoadResource
from ._size_rule import SizeRule
from ._parse_font import parseFont
from ._pen import emptyPen, textPen, dashPen, dotPen, parsePen, solidPen
from ._brush import emptyBrush, fillBrush
