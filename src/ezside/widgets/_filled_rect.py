"""The FilledRect subclass of BaseWidget provides a filled rectangle."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QColor, QPaintEvent, QPainter

from attribox import AttriBox

from ezside.core import parseColor, emptyPen

from ezside.widgets import BaseWidget


class FilledRect(BaseWidget):
  """The FilledRect subclass of BaseWidget provides a filled rectangle."""

  fillColor = AttriBox[QColor]()

  def __init__(self, *args, **kwargs) -> None:
    """The __init__ method initializes the FilledRect widget."""
    BaseWidget.__init__(self, *args, **kwargs)
    self.solidBrush.setColor(parseColor(self.fillColor))

  def paintEvent(self, event: QPaintEvent) -> None:
    """The paintEvent method is called when the widget needs to be
    repainted."""
    painter = QPainter()
    painter.begin(self)
    painter.setPen(emptyPen())
    painter.setBrush(self.solidBrush)
    painter.drawRoundedRect(self.rect(), 8, 8)
    painter.end()
