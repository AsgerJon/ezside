"""The 'ezside.tools' module provides functions streamlining the creation
of instances of QFont, QPen, QBrush and similar. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ._font import parseFont
from ._pen import emptyPen, textPen, dashPen, dotPen
from ._brush import emptyBrush, fillBrush
