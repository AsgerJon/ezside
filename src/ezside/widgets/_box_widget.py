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

from ezside.tools import fillBrush, emptyPen, SizeRule, MarginsBox, Align, \
  ColorBox

Rect: TypeAlias = Union[QRect, QRectF]

ic.configureOutput(includeContext=True)


class BoxWidget(QWidget):
  """BoxWidget provides a base class for other widgets that need to paint on
  a background that supports the box model."""

  margins = MarginsBox(1)
  paddings = MarginsBox(1)
  borders = MarginsBox(1)
  borderColor = ColorBox(QColor(0, 0, 0, 255))
  borderBrush = Field()
  backgroundColor = ColorBox(QColor(255, 255, 255, 255))
  backgroundBrush = Field()

  @borderBrush.GET
  def _getBorderBrush(self) -> QBrush:
    """Getter-function for the borderBrush."""
    return fillBrush(self.borderColor, )

  @backgroundBrush.GET
  def _getBackgroundBrush(self) -> QBrush:
    """Getter-function for the backgroundBrush."""
    return fillBrush(self.backgroundColor, )

  def paintEvent(self, event: QPaintEvent) -> None:
    """Paints the widget."""
    painter = QPainter()
    painter.begin(self)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    viewRect = painter.viewport()
    borderRect = QRectF.marginsRemoved(viewRect.toRectF(), self.borders)
    paddedRect = QRectF.marginsRemoved(borderRect, self.paddings)
    painter.setPen(emptyPen())
    painter.setBrush(self.borderBrush)
    painter.drawRect(borderRect)
    painter.setBrush(self.backgroundBrush)
    painter.drawRect(paddedRect)
    painter.end()
