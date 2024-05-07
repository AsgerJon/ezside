"""Label provides the general class for widgets whose primary function is
to display text. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtCore import Qt, QMargins, QRect, QPointF
from PySide6.QtGui import QFont, QPen, QColor, QBrush, QPaintEvent, QPainter
from attribox import AttriBox

from ezside.core import Normal, \
  SolidFill, \
  SolidLine, \
  AlignCenter, \
  emptyPen, \
  Center, AlignHCenter, AlignVCenter, AlignLeft, AlignRight, emptyBrush
from ezside.widgets import BaseWidget


class Label(BaseWidget):
  """Label provides the   general class for widgets"""

  __fallback_text__ = 'Label'

  text = AttriBox[str]('')

  def __init__(self, *args, **kwargs) -> None:
    posArgs = []
    iniText = None
    for arg in args:
      if isinstance(arg, str) and iniText is None:
        iniText = arg
      else:
        posArgs.append(arg)
    self.text = self.__fallback_text__ if iniText is None else iniText
    super().__init__(*posArgs, **kwargs)

  def getStyleFallbacks(self) -> dict[str, Any]:
    """Returns the style fallbacks for the Label."""
    font = QFont()
    font.setFamily('Montserrat')
    font.setPointSize(12)
    font.setWeight(Normal)
    textPen = QPen()
    textPen.setColor(QColor(0, 0, 0, 255))
    textPen.setStyle(Qt.PenStyle.SolidLine)
    textPen.setWidth(1)
    borderPen = QPen()
    borderPen.setColor(QColor(144, 144, 144, 255))
    borderPen.setStyle(SolidLine)
    borderPen.setWidth(2)
    backgroundBrush = QBrush()
    backgroundBrush.setColor(QColor(255, 255, 255, 255))
    backgroundBrush.setStyle(SolidFill)
    align = AlignCenter
    cornerRadius = 4
    margins = 2
    paddings = 2
    return {
      'font'           : font,
      'textPen'        : textPen,
      'borderPen'      : borderPen,
      'backgroundBrush': backgroundBrush,
      'align'          : align,
      'cornerRadius'   : cornerRadius,
      'margins'        : margins,
      'paddings'       : paddings,
    }

  def initStyle(self) -> None:
    """Initializes the styles. """

  def initUi(self) -> None:
    """Because the Label does not use layout or nested widgets,
    the implementation of this abstract method is empty."""

  def initSignalSlot(self) -> None:
    """Because the Label does not use signals or slots,
    the implementation of this abstract method is empty."""

  def _getKey(self) -> str:
    """Returns the key for the settings."""
    return 'label/%s' % self.styleId

  def _getOuterMargins(self) -> QMargins:
    """Returns the outer margins."""
    outerMargins = self.getStyle('outerMargins', QMargins(0, 0, 0, 0))
    return outerMargins

  def _getBorderWidth(self) -> int:
    """Returns the border width."""
    borderWidth = self.getStyle('borderWidth', 0)
    return borderWidth

  def _getBorderMargins(self) -> QMargins:
    """Returns the border margins."""
    width = self._getBorderWidth()
    return QMargins(width, width, width, width)

  def _getPadding(self, ) -> QMargins:
    """Returns the padding."""
    return self.getStyle('padding', QMargins(4, 4, 4, 4))

  def _getCornerRadius(self) -> int:
    """Returns the corner radius."""
    return self.getStyle('cornerRadius', 4)

  def _getBackgroundBrush(self) -> QBrush:
    """Returns the background brush."""
    fallbackBrush = QBrush()
    fallbackBrush.setStyle(SolidFill)
    fallbackBrush.setColor(QColor(225, 225, 225, 255, ))
    return self.getStyle('backgroundBrush', fallbackBrush)

  def _getBorderPen(self) -> QPen:
    """Returns the border pen."""
    fallbackPen = QPen()
    fallbackPen.setStyle(SolidLine)
    fallbackPen.setColor(QColor(63, 63, 63, 255))
    fallbackPen.setWidth(2)
    return self.getStyle('borderPen', fallbackPen)

  def _getTextPen(self) -> QPen:
    """Returns the text pen."""
    fallbackTextPen = QPen()
    fallbackTextPen.setStyle(SolidLine)
    fallbackTextPen.setColor(QColor(0, 0, 0, 255))
    fallbackTextPen.setWidth(1)
    return self.getStyle('textPen', fallbackTextPen)

  def _getFont(self) -> QFont:
    """Returns the font."""
    fallbackFont = QFont()
    fallbackFont.setFamily('Montserrat')
    fallbackFont.setPointSize(12)
    fallbackFont.setWeight(Normal)
    return self.getStyle('font', fallbackFont)

  def _getAlignRect(self, viewRect: QRect, movingRect: QRect) -> QRect:
    """Returns the moving rectangle aligned to the view rectangle given
    the current alignment settings"""
    movingSize = movingRect.size()
    hAlign = self.getStyle('hAlign', AlignLeft)
    vAlign = self.getStyle('vAlign', AlignVCenter)
    left, top = viewRect.left(), viewRect.top()
    if hAlign == AlignLeft:
      left += 0
    elif hAlign == AlignHCenter:
      left += (viewRect.width() - movingSize.width()) / 2
    elif hAlign == AlignRight:
      left += viewRect.width() - movingSize.width()
    if vAlign == AlignLeft:
      top += 0
    elif vAlign == AlignVCenter:
      top += (viewRect.height() - movingSize.height()) / 2
    elif vAlign == AlignRight:
      top += viewRect.height() - movingSize.height()
    topLeft = QPointF(left, top).toPoint()
    return QRect(topLeft, movingSize)

  def paintEvent(self, event: QPaintEvent) -> None:
    """Custom implementation of paint event"""
    painter = QPainter()
    painter.begin(self)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #  Collect shapes
    painter.setFont(self._getFont())  # Font must be set before boundingRect
    viewRect = painter.viewport()
    viewSize = viewRect.size()
    outerMargins = self._getOuterMargins()
    borderMargins = self._getBorderMargins()
    padding = self._getPadding()
    borderRect = viewRect.marginsRemoved(outerMargins)
    paddedRect = borderRect.marginsRemoved(borderMargins)
    innerRect = paddedRect.marginsRemoved(padding)
    textRect = painter.boundingRect(innerRect, Center, self.text)
    alignedRect = self._getAlignRect(innerRect, textRect)
    rectRadius = self._getCornerRadius()
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #  Fill background
    backgroundBrush = self._getBackgroundBrush()
    painter.setPen(emptyPen())
    painter.setBrush(backgroundBrush)
    painter.drawRoundedRect(innerRect, rectRadius, rectRadius)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #  Draw border
    borderPen = self._getBorderPen()
    painter.setPen(borderPen)
    painter.setBrush(emptyBrush())
    painter.drawRoundedRect(borderRect, rectRadius, rectRadius)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #  Print Text
    painter.setPen(self._getTextPen())
    painter.drawText(alignedRect, Center, self.text)
    painter.end()
