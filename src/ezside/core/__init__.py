"""The 'ezside.core' package provides a limited selection from the Qt
namespace in much shorter named versions. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ._qt_names import *
from ._resolve_font_enums import resolveFontFamily
from ._resolve_font_enums import resolveFontWeight, resolveFontCase
from ._resolve_align_enums import resolveAlign
from ._resolve_enum import resolveEnum
from ._parse_font import parseFont
from ._parse_pen import parsePen
from ._parse_brush import parseBrush

from ._colors import *

from ._pen import Pen
from ._brush import Brush
from ._parse_parent import parseParent
from ._font_family import Font

from ._color_factory import parseColor
from ._pen_factory import stylePen, emptyPen, solidPen
from ._pen_factory import dashPen, dotPen, dashDotPen
from ._brush_factory import emptyBrush, solidBrush
