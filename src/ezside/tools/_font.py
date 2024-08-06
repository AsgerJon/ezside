"""Font encapsulates settings for fonts and text rendering."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QColor, QFont, QPen, Qt, QPainter, QFontMetrics, \
  QFontMetricsF
from worktoy.desc import Field, AttriBox, DEFAULT
from worktoy.meta import BaseObject

from ezside.tools import FontWeight, FontFamily, FontCap, Align


class Font(BaseObject):
  """Font encapsulates settings for fonts and text rendering."""

  weight = AttriBox[FontWeight](FontWeight.NORMAL)
  size = AttriBox[int](12)
  family = AttriBox[FontFamily](FontFamily.COURIER)
  cap = AttriBox[FontCap](FontCap.MIX)
  italic = AttriBox[bool](False)
  underline = AttriBox[bool](False)
  strike = AttriBox[bool](False)
  align = AttriBox[Align](DEFAULT(Align.LEFT))
  color = AttriBox[QColor](QColor(0, 0, 0, 255))

  asQFont = Field()
  asQPen = Field()
  asQtAlign = Field()
  metrics = Field()

  @asQFont.GET
  def _getQFont(self) -> QFont:
    """Getter-function for QFont representation"""
    font = QFont()
    QFont.setFamily(font, self.family.value)
    QFont.setWeight(font, self.weight.qt)
    QFont.setCapitalization(font, self.cap.qt)
    QFont.setItalic(font, self.italic)
    QFont.setUnderline(font, self.underline)
    QFont.setStrikeOut(font, self.strike)
    QFont.setPointSize(font, self.size)
    return font

  @asQPen.GET
  def _getQPen(self) -> QPen:
    """Getter-function for QPen"""
    pen = QPen()
    pen.setStyle(Qt.PenStyle.SolidLine)
    pen.setWidth(1)
    pen.setColor(self.color)
    return pen

  @asQtAlign.GET
  def _getQtAlign(self) -> Qt.AlignmentFlag:
    """Getter-function for Qt.Alignment"""
    return self.align.qt

  def __matmul__(self, painter: QPainter) -> QPainter:
    """Applies itself to the painter and returns it """
    if not isinstance(painter, QPainter):
      return NotImplemented
    painter.setFont(self.asQFont)
    painter.setPen(self.asQPen)
    return painter

  def __rmatmul__(self, other) -> QPainter:
    """Applies itself to the painter and returns it """
    return self @ other

  @metrics.GET
  def _getMetrics(self) -> QFontMetricsF:
    """Getter-function for QFontMetrics"""
    return QFontMetricsF(self.asQFont)
