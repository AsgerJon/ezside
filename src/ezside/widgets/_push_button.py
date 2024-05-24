"""PushButton provides a descriptor class for push buttons. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QBrush, QColor
from attribox import AttriBox
from vistutils.fields import EmptyField

from ezside.desc import parseBrush, SolidFill


class PushButtonWidget(CanvasWidget):
  """PushButtonWidget provides a widget class for push buttons. """

  __is_enabled__ = None
  __is_hovered__ = None
  __is_pressed__ = None

  buttonText = AttriBox[str]()

  marginBrush = EmptyField()

  def getBackgroundBrush(self) -> QBrush:
    """Returns the margin brush."""
    if self.__is_enabled__:
      color = QColor(239, 239, 239, 255)
    else:
      color = QColor(247, 247, 247, 255)
    if self.__is_pressed__:
      color = color.darker(125)
    elif self.__is_hovered__:
      color = color.darker(110)
    return parseBrush(color, SolidFill)
