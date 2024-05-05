"""Label provides the general class for widgets whose primary function is
to display text. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations
from typing import TYPE_CHECKING, Any

from PySide6.QtCore import Qt, QSettings
from PySide6.QtGui import QFont, QPen, QColor, QBrush
from attribox import AttriBox

from ezside.core import Normal, DemiBold, Bold, SolidFill, SolidLine, \
  AlignVCenter, AlignHCenter, AlignCenter
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
    settings = QSettings()
    settings.value()

  def initUi(self) -> None:
    """Because the Label does not use layout or nested widgets,
    the implementation of this abstract method is empty."""
    pass
