"""Label provides the general class for widgets whose primary function is
to display text. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtCore import Qt, QMargins, QRect, QPointF
from PySide6.QtGui import QFont, QPen, QColor, QBrush, QPaintEvent, QPainter
from attribox import AttriBox
from vistutils.text import monoSpace

from ezside.core import Normal, \
  SolidFill, \
  SolidLine, \
  AlignCenter, \
  emptyPen, \
  Center, \
  AlignHCenter, \
  AlignVCenter, \
  AlignLeft, \
  AlignRight, \
  emptyBrush, \
  AlignTop, AlignBottom
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

  @classmethod
  def registerStyleIds(cls) -> list[str]:
    """Registers the supported style IDs for Label."""
    return ['title', 'warning', 'normal']

  @classmethod
  def registerStates(cls) -> list[str]:
    """Registers the supported states for Label."""
    return ['base', 'focus']

  @classmethod
  def registerFields(cls) -> dict[str, Any]:
    """Registers default field values for Label, providing a foundation
    for customization across different styleIds and states."""
    return {
      'fontSize'           : 12,
      'fontWeight'         : QFont.Weight.Normal,
      'fontCapitalization' : QFont.Capitalization.MixedCase,
      # Options: QFont.Capitalization.MixedCase, 'capitalize',
      # QFont.Capitalization.SmallCaps, 'lowercase'
      'textColor'          : QColor(0, 0, 0),  # Default black text
      'backgroundColor'    : QColor(255, 255, 255),
      'borderColor'        : QColor(0, 0, 0),
      # Default white background
      'borderCornerRadius' : 5,
      'margins'            : QMargins(5, 5, 5, 5),
      'borders'            : QMargins(1, 1, 1, 1),
      'paddings'           : QMargins(5, 5, 5, 5),
      'horizontalAlignment': AlignHCenter,
      'verticalAlignment'  : AlignVCenter
    }

  @classmethod
  def registerDynamicFields(cls) -> dict[str, Any]:
    """Defines dynamic fields based on styleId and state. These settings
    override the base field values in specific styles and states."""
    return {
      'title'  : {
        'base' : {
          'fontSize'          : 18,
          'fontWeight'        : QFont.Weight.Bold,
          'fontCapitalization': QFont.Capitalization.SmallCaps,
          'textColor'         : QColor(25, 50, 75),
          'backgroundColor'   : QColor(230, 240, 250),
          'borderCornerRadius': 0,
          'margins'           : QMargins(10, 10, 10, 10),
          'borders'           : QMargins(2, 2, 2, 2),
          'paddings'          : QMargins(10, 10, 10, 10)
        },
        'focus': {
          'fontSize'          : 18,
          'fontWeight'        : QFont.Weight.Bold,
          'fontCapitalization': QFont.Capitalization.SmallCaps,
          'textColor'         : QColor(25, 50, 75),
          'backgroundColor'   : QColor(210, 220, 230),
          'borderCornerRadius': 0,
          'margins'           : QMargins(12, 12, 12, 12),
          'borders'           : QMargins(3, 3, 3, 3),
          'paddings'          : QMargins(12, 12, 12, 12)
        }
      },
      'warning': {
        'base' : {
          'fontSize'          : 16,
          'fontWeight'        : QFont.Weight.Bold,
          'fontCapitalization': QFont.Capitalization.SmallCaps,
          'textColor'         : QColor(255, 255, 255),
          'backgroundColor'   : QColor(255, 165, 0),  # Orange
          'borderCornerRadius': 10,
          'margins'           : QMargins(8, 8, 8, 8),
          'borders'           : QMargins(1, 1, 1, 1),
          'paddings'          : QMargins(8, 8, 8, 8)
        },
        'focus': {
          'fontSize'          : 16,
          'fontWeight'        : QFont.Weight.Bold,
          'fontCapitalization': QFont.Capitalization.SmallCaps,
          'textColor'         : QColor(255, 255, 255),
          'backgroundColor'   : QColor(255, 140, 0),  # Dark orange
          'borderCornerRadius': 10,
          'margins'           : QMargins(10, 10, 10, 10),
          'borders'           : QMargins(2, 2, 2, 2),
          'paddings'          : QMargins(10, 10, 10, 10)
        }
      },
      'normal' : {
        'base' : {
          'fontSize'          : 12,
          'fontWeight'        : QFont.Weight.Normal,
          'fontCapitalization': QFont.Capitalization.MixedCase,
          'textColor'         : QColor(0, 0, 0),
          'backgroundColor'   : QColor(255, 255, 255),
          'borderCornerRadius': 5,
          'margins'           : QMargins(5, 5, 5, 5),
          'borders'           : QMargins(1, 1, 1, 1),
          'paddings'          : QMargins(5, 5, 5, 5)
        },
        'focus': {
          'fontSize'          : 12,
          'fontWeight'        : QFont.Weight.Normal,
          'fontCapitalization': QFont.Capitalization.MixedCase,
          'textColor'         : QColor(0, 0, 0),
          'backgroundColor'   : QColor(245, 245, 245),  # Light grey
          'borderCornerRadius': 5,
          'margins'           : QMargins(7, 7, 7, 7),
          'borders'           : QMargins(2, 2, 2, 2),
          'paddings'          : QMargins(7, 7, 7, 7)
        }
      }
    }

  def _getFont(self) -> QFont:
    """Instantiates QFont based on current state and styleId"""
    fontSize = self._getFieldValue('fontSize')
    fontWeight = self._getFieldValue('fontWeight')
    fontCapitalization = self._getFieldValue('fontCapitalization')
    font = QFont()
    font.setPointSize(fontSize)
    font.setWeight(fontWeight)
    font.setCapitalization(fontCapitalization)
    return font

  def _getTextPen(self) -> QPen:
    """Instantiates QPen for text based on current state and styleId"""
    textColor = self._getFieldValue('textColor')
    pen = QPen()
    pen.setStyle(SolidLine)
    pen.setWidth(1)
    pen.setColor(textColor)
    return pen

  def _getBackgroundBrush(self) -> QBrush:
    """Instantiates QBrush for background based on current state and
    styleId"""
    backgroundColor = self._getFieldValue('backgroundColor')
    brush = QBrush()
    brush.setStyle(SolidFill)
    brush.setColor(backgroundColor)
    return brush

  def _getBorderPen(self) -> QPen:
    """Instantiates QPen for border based on current state and styleId"""
    borderColor = self._getFieldValue('textColor')
    pen = QPen()
    pen.setStyle(SolidLine)
    pen.setWidth(1)
    pen.setColor(borderColor)
    return pen

  def _getBorderBrush(self) -> QBrush:
    """Instantiates QBrush for border based on current state and styleId"""
    borderColor = self._getFieldValue('borderColor')
    brush = QBrush()
    brush.setStyle(SolidFill)
    brush.setColor(borderColor)
    return brush

  def _getAlignedRect(self, staticRect: QRect, movingRect: QRect) -> QRect:
    """Calculates the aligned rectangle for text"""
    vAlign = self._getFieldValue('verticalAlignment')
    hAlign = self._getFieldValue('horizontalAlignment')
    movingSize = movingRect.size()
    staticHeight, movingHeight = staticRect.height(), movingRect.height()
    staticWidth, movingWidth = staticRect.width(), movingRect.width()
    if vAlign == AlignTop:
      top = staticRect.top()
    elif vAlign in [AlignCenter, AlignVCenter]:
      top = staticRect.top() + (staticHeight - movingHeight) / 2
    elif vAlign == AlignBottom:
      top = staticRect.bottom() - movingHeight
    else:
      e = """Unrecognized value for vertical alignment: '%s'"""
      raise ValueError(monoSpace(e % str(vAlign)))
    if hAlign == AlignLeft:
      left = staticRect.left()
    elif hAlign in [AlignCenter, AlignHCenter]:
      left = staticRect.left() + (staticWidth - movingWidth) / 2
    elif hAlign == AlignRight:
      left = staticRect.right() - movingWidth
    else:
      e = """Unrecognized value for horizontal alignment: '%s'"""
      raise ValueError(monoSpace(e % str(hAlign)))
    topLeft = QPointF(left, top).toPoint()
    return QRect(topLeft, movingSize)

  def paintEvent(self, event: QPaintEvent) -> None:
    """Custom implementation of paint event"""
    painter = QPainter()
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #  Request data

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #  Collect shapes
    painter.begin(self)
    painter.setFont(self._getFont())  # Font must be set before boundingRect
    viewRect = painter.viewport()
    viewSize = viewRect.size()
    outerMargins = self._getFieldValue('margins')
    borderMargins = self._getFieldValue('borders')
    padding = self._getFieldValue('paddings')
    borderRect = viewRect.marginsRemoved(outerMargins)
    paddedRect = borderRect.marginsRemoved(borderMargins)
    innerRect = paddedRect.marginsRemoved(padding)
    textRect = painter.boundingRect(innerRect, Center, self.text)
    alignedRect = self._getAlignedRect(innerRect, textRect)
    cornerRadius = self._getFieldValue('borderCornerRadius')
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #  Fill background including border
    borderBrush = self._getBorderBrush()
    painter.setPen(emptyPen())
    painter.setBrush(borderBrush)
    painter.drawRoundedRect(borderRect, cornerRadius, cornerRadius)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #  Fill background excluding border
    backgroundBrush = self._getBackgroundBrush()
    painter.setPen(emptyPen())
    painter.setBrush(backgroundBrush)
    painter.drawRoundedRect(innerRect, cornerRadius, cornerRadius)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #  Print Text
    painter.setPen(self._getTextPen())
    painter.drawText(alignedRect, Center, self.text)
    painter.end()
