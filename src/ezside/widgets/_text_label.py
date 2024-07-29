"""TextLabel provides a property driven alternative to QLabel. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Never

from PySide6.QtCore import QSize, QSizeF, QRect, QMargins, QRectF
from PySide6.QtGui import (QFont, QFontMetrics, QPaintEvent, QPainter,
                           QColor, QPen)
from PySide6.QtWidgets import QWidget, QSizePolicy
from worktoy.desc import AttriBox, EmptyField
from worktoy.parse import maybe
from worktoy.text import typeMsg

from ezside.tools import textPen, Align, emptyBrush
from ezside.widgets import BoxWidget


class TextLabel(BoxWidget):
  """TextLabel provides a property driven alternative to QLabel. """

  __fallback_weight__ = QFont.Weight.Normal
  __font_weight__ = None
  __text_alignment__ = None

  text = AttriBox[str]('LMAO')
  textColor = AttriBox[QColor](QColor(0, 0, 0, 255))
  fontFamily = AttriBox[str]('Courier')
  fontSize = AttriBox[int](12)

  alignment = EmptyField()
  fontWeight = EmptyField()
  textFont = EmptyField()
  metrics = EmptyField()
  textRect = EmptyField()
  pen = EmptyField()

  @alignment.GET
  def _getAlignment(self) -> Align:
    """This method returns the alignment of the text label. """
    alignment = maybe(self.__text_alignment__, Align.CENTER)
    if isinstance(alignment, Align):
      return alignment
    e = typeMsg('alignment', alignment, Align)
    raise TypeError(e)

  @alignment.SET
  def _setAlignment(self, alignment: Align) -> None:
    """This method sets the alignment of the text label. """
    if not isinstance(alignment, Align):
      e = typeMsg('alignment', alignment, Align)
      raise TypeError(e)
    self.__text_alignment__ = alignment

  @fontWeight.GET
  def _getFontWeight(self) -> QFont.Weight:
    """This method returns the font weight of the text label. """
    weight = maybe(self.__font_weight__, self.__fallback_weight__)
    if isinstance(weight, QFont.Weight):
      return weight
    e = typeMsg('weight', weight, QFont.Weight)
    raise TypeError(e)

  @fontWeight.SET
  def _setFontWeight(self, weight: QFont.Weight) -> None:
    """This method sets the font weight of the text label. """
    if not isinstance(weight, QFont.Weight):
      e = typeMsg('weight', weight, QFont.Weight)
      raise TypeError(e)
    self.__font_weight__ = weight

  @textFont.GET
  def _getFont(self) -> QFont:
    """This method returns the font used by the text label. """
    out = QFont()
    out.setFamily(self.fontFamily)
    out.setPointSize(self.fontSize)
    return out

  @textFont.SET
  def _setFont(self, font: QFont) -> None:
    """This method decomposes the font into its components and sets
    relevant attributes to match. """
    if not isinstance(font, QFont):
      e = typeMsg('font', font, QFont)
      raise TypeError(e)
    family = QFont.family(font)
    size = QFont.pointSize(font)
    weight = QFont.weight(font)
    self.fontFamily = family
    self.fontSize = size
    self.fontWeight = weight

  @metrics.GET
  def _getMetrics(self) -> QFontMetrics:
    """This method returns the font metrics of the text label. """
    return QFontMetrics(self.textFont)

  @textRect.GET
  def _getBoundingRect(self) -> QRect:
    """This method returns the bounding size of the text with the given
    font. """
    rect = self.metrics.boundingRect(self.contentRect, 0, self.text)
    return self.alignment.fitRect(rect, self.contentRect)

  @pen.GET
  def _getTextPen(self) -> QPen:
    """This method returns the pen used to draw the text. """
    return textPen(self.textColor)

  @alignment.DELETE
  @textRect.SET
  @textRect.DELETE
  @metrics.SET
  @metrics.DELETE
  @pen.SET
  @pen.DELETE
  @textFont.DELETE
  @fontWeight.DELETE
  def _badAccessor(self, *_) -> Never:
    """Illegal accessor function"""
    e = """Tried illegally accessing an attribute!"""
    raise TypeError(e)

  @text.ONSET
  def _handleNewText(self, *args) -> None:
    """This method is triggered when the text at the text field is
    changed. """

  def __init__(self, *args, **kwargs) -> None:
    parent, text = None, None
    for arg in args:
      if isinstance(arg, QWidget) and parent is None:
        parent = arg
      if isinstance(arg, str) and text is None:
        text = arg
      if parent is not None and text is not None:
        BoxWidget.__init__(self, parent)
        self.text = text
        break
    else:
      if parent is None:
        BoxWidget.__init__(self, )
      else:
        BoxWidget.__init__(self, parent)
    self._handleNewText()
    self.backgroundColor = QColor(191, 191, 191, 255)
    self.borderColor = QColor(0, 0, 0, 255)
    self.padding = QMargins(4, 4, 4, 4, )
    policy = QSizePolicy()
    policy.setVerticalPolicy(QSizePolicy.Policy.Maximum)
    policy.setHorizontalPolicy(QSizePolicy.Policy.Maximum)
    self.setSizePolicy(policy)

  def sizeHint(self) -> QSize:
    """This method returns the size hint of the widget."""
    return self.textRect.size()

  def minimumSizeHint(self) -> QSize:
    """This method returns the minimum size hint of the widget."""
    return self.sizeHint()

  def paintEvent(self, event: QPaintEvent) -> None:
    """Implementation of the paint event"""
    BoxWidget.paintEvent(self, event)
    painter = QPainter()
    painter.begin(self)
    painter.setFont(self.textFont)
    painter.setPen(self.pen)
    painter.setBrush(emptyBrush())
    painter.drawText(self.textRect, 0, self.text)
    painter.end()
