"""The 'ezside.core' package provides a limited selection from the Qt
namespace in much shorter named versions."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ._parse_rect import parseKwargsSourceTargetRect, parseRect
from ._parse_style_id import parseStyleId
from ._qt_names import *
from ._resolve_enum import resolveEnum
from ._parse_alignments import parseAlignment
from ._alignment_descriptor import Alignment
from ._align_rect import alignRect
from ._parse_margins import parseMargins
from ._margins_descriptor import Margins
from ._parse_orientation import parseOrientation
from ._orientation_descriptor import Orientation
from ._parse_line_length import parseLineLength
from ._parse_text import parseText
from ._cursor_vector import CursorVector
from ._ez_timer import EZTimer
from ._resolve_font_enums import resolveFontFamily
from ._resolve_font_enums import resolveFontWeight, resolveFontCase
from ._resolve_align_enums import resolveAlign
from ._parse_font import parseFont
from ._parse_pen import parsePen, emptyPen
from ._parse_brush import parseBrush, emptyBrush

from ._colors import *

from ._parse_parent import parseParent
