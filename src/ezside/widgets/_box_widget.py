"""BoxWidget provides a base class for other widgets that need to paint on
a background that supports the box model."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TypeAlias, Union, Never

from PySide6.QtCore import QMargins, QRect, QRectF, QPointF, QSizeF
from PySide6.QtCore import QMarginsF
from PySide6.QtGui import QPaintEvent, QPainter, QColor, QBrush
from PySide6.QtWidgets import QWidget
from icecream import ic
from worktoy.desc import AttriBox, Field
from worktoy.parse import maybe
from worktoy.text import monoSpace, typeMsg

from ezside.tools import fillBrush, emptyPen, SizeRule

Rect: TypeAlias = Union[QRect, QRectF]

ic.configureOutput(includeContext=True)


class BoxWidget(QWidget):
  """BoxWidget provides a base class for other widgets that need to paint on
  a background that supports the box model."""
