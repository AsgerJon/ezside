"""Label provides the general class for widgets whose primary function is
to display text. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtCore import QMargins, QRect, QPointF, QPoint
from PySide6.QtGui import QFont, QPen, QColor, QBrush, QPaintEvent, QPainter
from attribox import AttriBox
from vistutils.text import monoSpace

from ezside.core import Normal, SolidFill, SolidLine, AlignCenter
from ezside.core import emptyPen, Center, AlignHCenter, AlignVCenter
from ezside.core import AlignLeft, AlignRight, AlignTop
from ezside.core import AlignBottom, Cap, Weight, SmallCaps, Bold, MixCase
from ezside.widgets import BaseWidget


class Label(BaseWidget):
  """Label provides the   general class for widgets"""

  def initUi(self) -> None:
    """Initializes the user interface."""

  def initSignalSlot(self) -> None:
    """Connects signals and slots"""

  def detectState(self) -> str:
    """State detector"""
    return 'base'

  __fallback_text__ = 'Label'

  text = AttriBox[str]('')

  @staticmethod
  def parseFont(size: int, weight: Weight, cap: Cap) -> QFont:
    """Parses the arguments to a QFont"""
    font = QFont()
    font.setPointSize(size)
    font.setWeight(weight)
    font.setCapitalization(cap)
    return font

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
      'font'               : cls.parseFont(12, Normal, MixCase),
      'textColor'          : QColor(0, 0, 0),  # Default black text
      'backgroundColor'    : QColor(255, 255, 255),
      'borderColor'        : QColor(0, 0, 0),
      # Default white background
      'borderCornerRadius' : QPoint(5, 5),
      'margins'            : QMargins(5, 5, 5, 5),
      'borders'            : QMargins(1, 1, 1, 1),
      'paddings'           : QMargins(5, 5, 5, 5),
      'horizontalAlignment': 'center',
      'verticalAlignment'  : 'center'
    }

  @classmethod
  def registerDynamicFields(cls) -> dict[str, Any]:
    """Defines dynamic fields based on styleId and state. These settings
    override the base field values in specific styles and states."""
    return {
      'title'  : {
        'base' : {
          'font'              : cls.parseFont(18, Bold, SmallCaps),
          'textColor'         : QColor(25, 50, 75),
          'backgroundColor'   : QColor(230, 240, 250),
          'borderCornerRadius': QPoint(0, 0),
          'margins'           : QMargins(10, 10, 10, 10),
          'borders'           : QMargins(2, 2, 2, 2),
          'paddings'          : QMargins(10, 10, 10, 10)
        },
        'focus': {
          'font'              : cls.parseFont(18, Bold, SmallCaps),
          'textColor'         : QColor(25, 50, 75),
          'backgroundColor'   : QColor(210, 220, 230),
          'borderCornerRadius': QPoint(0, 0),
          'margins'           : QMargins(12, 12, 12, 12),
          'borders'           : QMargins(3, 3, 3, 3),
          'paddings'          : QMargins(12, 12, 12, 12)
        }
      },
      'warning': {
        'base' : {
          'font'              : cls.parseFont(16, Bold, SmallCaps),
          'textColor'         : QColor(255, 255, 255),
          'backgroundColor'   : QColor(255, 165, 0),
          'borderCornerRadius': QPoint(0, 0),
          'margins'           : QMargins(8, 8, 8, 8),
          'borders'           : QMargins(1, 1, 1, 1),
          'paddings'          : QMargins(8, 8, 8, 8)
        },
        'focus': {
          'font'              : cls.parseFont(16, Bold, SmallCaps),
          'textColor'         : QColor(255, 255, 255),
          'backgroundColor'   : QColor(255, 140, 0),
          'borderCornerRadius': QPoint(0, 0),
          'margins'           : QMargins(10, 10, 10, 10),
          'borders'           : QMargins(2, 2, 2, 2),
          'paddings'          : QMargins(10, 10, 10, 10)
        }
      },
      'normal' : {
        'base' : {
          'font'              : cls.parseFont(12, Normal, MixCase),
          'textColor'         : QColor(0, 0, 0),
          'backgroundColor'   : QColor(255, 255, 255),
          'borderCornerRadius': QPoint(0, 0),
          'margins'           : QMargins(5, 5, 5, 5),
          'borders'           : QMargins(1, 1, 1, 1),
          'paddings'          : QMargins(5, 5, 5, 5)
        },
        'focus': {
          'font'              : cls.parseFont(12, Normal, MixCase),
          'textColor'         : QColor(0, 0, 0),
          'backgroundColor'   : QColor(245, 245, 245),
          'borderCornerRadius': QPoint(5, 5),
          'margins'           : QMargins(7, 7, 7, 7),
          'borders'           : QMargins(2, 2, 2, 2),
          'paddings'          : QMargins(7, 7, 7, 7)
        }
      }
    }

  def _getFont(self) -> QFont:
    """Instantiates QFont based on current state and styleId"""
    return self._getStyle('font')

  def _getTextPen(self) -> QPen:
    """Instantiates QPen for text based on current state and styleId"""
    textColor = self._getStyle('textColor')
    pen = QPen()
    pen.setStyle(SolidLine)
    pen.setWidth(1)
    pen.setColor(textColor)
    return pen

  def _getBackgroundBrush(self) -> QBrush:
    """Instantiates QBrush for background based on current state and
    styleId"""
    backgroundColor = self._getStyle('backgroundColor')
    brush = QBrush()
    brush.setStyle(SolidFill)
    brush.setColor(backgroundColor)
    return brush

  def _getBorderPen(self) -> QPen:
    """Instantiates QPen for border based on current state and styleId"""
    borderColor = self._getStyle('textColor')
    pen = QPen()
    pen.setStyle(SolidLine)
    pen.setWidth(1)
    pen.setColor(borderColor)
    return pen

  def _getBorderBrush(self) -> QBrush:
    """Instantiates QBrush for border based on current state and styleId"""
    borderColor = self._getStyle('borderColor')
    brush = QBrush()
    brush.setStyle(SolidFill)
    brush.setColor(borderColor)
    return brush

  def _getAlignedRect(self, staticRect: QRect, movingRect: QRect) -> QRect:
    """Calculates the aligned rectangle for text"""
    vAlign = self._getStyle('verticalAlignment')
    hAlign = self._getStyle('horizontalAlignment')
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
    outerMargins = self._getStyle('margins')
    borderMargins = self._getStyle('borders')
    padding = self._getStyle('paddings')
    borderRect = viewRect.marginsRemoved(outerMargins)
    paddedRect = borderRect.marginsRemoved(borderMargins)
    innerRect = paddedRect.marginsRemoved(padding)
    textRect = painter.boundingRect(innerRect, Center, self.text)
    alignedRect = self._getAlignedRect(innerRect, textRect)
    cornerRadius = self._getStyle('borderCornerRadius')
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
