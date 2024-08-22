"""Font encapsulates settings for fonts and text rendering."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Callable

from PySide6.QtCore import QSizeF, QRectF
from PySide6.QtGui import QColor, QFont, QPen, Qt, QPainter, QFontMetricsF
from icecream import ic
from worktoy.desc import Field, AttriBox, DEFAULT
from worktoy.meta import BaseObject
from worktoy.parse import maybeType

from ezside.tools import FontWeight, FontFamily, FontCap, Align, ColorBox

ic.configureOutput(includeContext=True)


class Font(BaseObject):
  """Font encapsulates settings for fonts and text rendering."""

  weight = AttriBox[FontWeight](FontWeight.NORMAL)
  size = AttriBox[int](12)
  family = AttriBox[FontFamily](FontFamily.COURIER)
  cap = AttriBox[FontCap](FontCap.MIX)
  italic = AttriBox[bool](False)
  underline = AttriBox[bool](False)
  strike = AttriBox[bool](False)
  align = AttriBox[Align](DEFAULT(Align.CENTER))
  color = ColorBox(QColor(0, 0, 0, 255))

  asQFont = Field()
  asQPen = Field()
  asQtAlign = Field()
  metrics = Field()
  boundSize = Field()
  boundRect = Field()

  @boundSize.GET
  def _getBoundSize(self) -> Callable:
    """Getter-function for QFontMetrics"""

    def callMeMaybe(text: str) -> QSizeF:
      """Returns the bounding rectangle of the text"""
      return self.metrics.boundingRect(text).size()

    return callMeMaybe

  @boundRect.GET
  def _getBoundRect(self) -> Callable:
    """Getter-function for bounding rect function"""

    def callMeMaybe(text: str) -> QRectF:
      """Returns the bounding rectangle of the text"""
      return self.metrics.boundingRect(text)

    return callMeMaybe

  @asQFont.GET
  def _getQFont(self) -> QFont:
    """Getter-function for QFont representation"""
    out = QFont()
    QFont.setFamily(out, self.family.value)
    QFont.setWeight(out, self.weight.qt)
    QFont.setCapitalization(out, self.cap.qt)
    QFont.setItalic(out, self.italic)
    QFont.setUnderline(out, self.underline)
    QFont.setStrikeOut(out, self.strike)
    QFont.setPointSize(out, self.size)
    return out

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

  @classmethod
  def fromJSON(cls, data: dict) -> Font:
    """Creates a Font object from JSON data"""
    newFont = cls()
    for (key, value) in data.items():
      if hasattr(newFont, key):
        setattr(newFont, key, value)
    return newFont

  def __init__(self, *args) -> None:
    self.size = maybeType(int, *args, 12)
    for arg in args:
      if isinstance(arg, FontFamily):
        self.family = arg
      if isinstance(arg, FontWeight):
        self.weight = arg
      if isinstance(arg, FontCap):
        self.cap = arg
      if isinstance(arg, Align):
        self.align = arg
