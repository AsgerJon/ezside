"""FontStyle provides settings for widgets printing text."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic
from typing import TypeAlias, Union, Callable

from PySide6.QtCore import QSizeF, QRectF, QSize, QRect
from PySide6.QtGui import QFont, Qt, QPainter, QFontMetricsF
from PySide6.QtGui import QColor, QPen
from worktoy.desc import Field, AttriBox, DEFAULT
from worktoy.text import typeMsg

from ezside.style import Align, AbstractStyle
from ezside.style.font_enums import FontFamily, FontWeight, FontCap

ic.configureOutput(includeContext=True)

Data: TypeAlias = dict[str, Union[str, dict]]


class FontStyle(AbstractStyle):
  """FontStyle provides settings for widgets printing text."""

  weight = AttriBox[FontWeight](FontWeight.NORMAL)
  size = AttriBox[int](12)
  family = AttriBox[FontFamily](FontFamily.COURIER)
  cap = AttriBox[FontCap](FontCap.MIX)
  italic = AttriBox[bool](False)
  underline = AttriBox[bool](False)
  strike = AttriBox[bool](False)

  textRed = AttriBox[int](0)
  textGreen = AttriBox[int](0)
  textBlue = AttriBox[int](0)
  textAlpha = AttriBox[int](255)

  textColor = Field()
  textPen = Field()

  asQFont = Field()
  asQPen = Field()
  asQtAlign = Field()
  metrics = Field()

  def boundSize(self, text: str) -> QSizeF:
    """Returns the bounding rectangle of the text"""
    rect = self.metrics.boundingRect(text)
    if isinstance(rect, QRectF):
      return rect.size()
    if isinstance(rect, QRect):
      return QSize.toSizeF(rect.size())
    e = typeMsg('rect', rect, QRectF)
    raise TypeError(e)

  def boundRect(self, text: str) -> QRectF:
    """Returns the bounding rectangle of the text"""
    return self.metrics.boundingRect(text)

  @textColor.GET
  def _getTextColor(self) -> QColor:
    """Getter-function for the textColor."""
    textColor = QColor(self.textRed,
                       self.textGreen,
                       self.textBlue,
                       self.textAlpha)
    return textColor

  @textColor.SET
  def _setTextColor(self, value: object) -> None:
    """Setter-function for the textColor."""
    red, green, blue, alpha = self._parseColor(value)
    self.textRed = red
    self.textGreen = green
    self.textBlue = blue
    self.textAlpha = alpha

  @textPen.GET
  def _getTextPen(self) -> QPen:
    """Getter-function for the textPen."""
    pen = QPen()
    pen.setColor(self.textColor)
    return pen

  @classmethod
  def load(cls, data: Data) -> FontStyle:
    """Load the style data from the given dictionary into a new instance. """
    newFont = cls()
    weightKey = data.get('weight', 'normal')
    newFont.weight = FontWeight(weightKey)
    sizeKey = data.get('size', '12')
    newFont.size = int(sizeKey)
    familyKey = data.get('family', 'courier')
    newFont.family = FontFamily(familyKey)
    capKey = data.get('cap', 'mix')
    newFont.cap = FontCap(capKey)
    newFont.italic = data.get('italic', False)
    newFont.underline = data.get('underline', False)
    newFont.strike = data.get('strike', False)
    colorKey = data.get('textColor', {})
    newFont.textColor = colorKey
    return newFont

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
    pen.setColor(self.textColor)
    return pen

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
