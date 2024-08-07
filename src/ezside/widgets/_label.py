"""Label provides a property driven alternative to QLabel. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Never, Any

from PySide6.QtCore import QSize, QRect, QMargins, Qt, QPoint, QMarginsF, \
  QRectF, QSizeF
from PySide6.QtGui import (QFont, QFontMetrics, QPaintEvent, QPainter,
                           QColor, QPen, QFontMetricsF)
from PySide6.QtWidgets import QWidget, QGridLayout
from icecream import ic
from worktoy.desc import AttriBox, Field, DEFAULT
from worktoy.meta import overload, BaseObject
from worktoy.parse import maybe
from worktoy.text import typeMsg, monoSpace

from ezside.tools import textPen, Align, emptyBrush, fillBrush, parsePen, \
  Font, FontFamily, FontCap
from ezside.widgets import BoxWidget

ic.configureOutput(includeContext=True)


class Label(BoxWidget):
  """Label provides a property driven alternative to QLabel. """

  __fallback_text__ = 'LABEL'
  __parsed_object__ = None

  textFont = AttriBox[Font](16, FontFamily.MONTSERRAT, FontCap.MIX)
  text = AttriBox[str]()

  def requiredSize(self) -> QSizeF:
    """The required size to show the current text with the current font."""
