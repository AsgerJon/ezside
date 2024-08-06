"""Label provides a property driven alternative to QLabel. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Never

from PySide6.QtCore import QSize, QRect, QMargins, Qt, QPoint, QMarginsF, \
  QRectF, QSizeF
from PySide6.QtGui import (QFont, QFontMetrics, QPaintEvent, QPainter,
                           QColor, QPen, QFontMetricsF)
from PySide6.QtWidgets import QWidget, QGridLayout
from icecream import ic
from worktoy.desc import AttriBox, Field, DEFAULT
from worktoy.parse import maybe
from worktoy.text import typeMsg

from ezside.tools import textPen, Align, emptyBrush, fillBrush, parsePen, \
  Font
from ezside.widgets import BoxWidget

ic.configureOutput(includeContext=True)


class Label(BoxWidget):
  """Label provides a property driven alternative to QLabel. """

  font = AttriBox[Font]()
  text = AttriBox[str](DEFAULT('LMAO'))

  rectSize = Field()

  @rectSize.GET
  def _getRectSize(self) -> QSizeF:
    """This method calculates the size required to bound the text."""
    return QFontMetricsF.boundingRect(self.font.metrics, self.text).size()

  def minimumSizeHint(self) -> QSize:
    """This method returns the size hint of the widget."""
    return QSizeF(self.rectSize.width(), self.rectSize.height()).toSize()
