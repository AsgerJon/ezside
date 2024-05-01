"""TextPen provides the QPen instance to be used by"""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QPen
from attribox import AttriBox

from ezside.style import RGB
from ezside.widgets import BaseWidget


class TextPen:
  """TextPen provides the QPen instance to be used by"""

  color = AttriBox[RGB](0, 0, 0, )

  def getPen(self, ) -> QPen:
    """getPen returns the QPen instance"""
    pen = QPen()
    pen.setStyle(Qt.PenStyle.SolidLine)
    pen.setColor(self.color.getQColor())
    return pen
