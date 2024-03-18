"""BorderRect provides a bordered rectangle with no fill."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QPaintEvent, QPainter

from ezqt.core import emptyBrush
from ezqt.widgets import BaseWidget


class BorderRect(BaseWidget):
  """BorderRect provides a bordered rectangle with no fill."""

  def __init__(self, *args, **kwargs) -> None:
    BaseWidget.__init__(self, *args, **kwargs)

  def paintEvent(self, event: QPaintEvent) -> None:
    """The paintEvent method is called when the widget needs to be
    repainted."""
    painter = QPainter()
    painter.begin(self)
    painter.setPen(self.pen)
    painter.setBrush(emptyBrush())
    painter.drawRect(self.rect())
    painter.end()
