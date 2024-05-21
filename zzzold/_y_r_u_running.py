"""YRURunning provides an animated widget indicating visually the speed at
which a signal is being emitted."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from math import cos, sin, pi
import time
from typing import TYPE_CHECKING

from PySide6.QtCore import QPointF, QLineF
from PySide6.QtGui import QColor
from icecream import ic

from ezside.core import parseBrush, emptyPen, emptyBrush, SolidFill, parsePen
from ezside.core import parseParent
from ezside.widgets import CanvasWidget, GraffitiVandal

ic.configureOutput(includeContext=True, )

if TYPE_CHECKING:
  pass


class YRURunning(CanvasWidget):
  """YRURunning provides an animated widget indicating visually the speed at
  which a signal is being emitted."""
  
  def customPaint(self, painter: GraffitiVandal) -> None:
    """Painting the dedicated area of the widget."""
    r = painter.viewport().width() / 2
    origin = painter.viewport().center()
    theta = time.perf_counter() * 2 * pi
    periphery = QPointF(r * cos(theta), r * sin(theta))
    painter.setBrush(parseBrush(QColor(144, 255, 0, 255)))
    painter.setPen(emptyPen())
    painter.drawEllipse(origin, r, r)
    painter.setBrush(emptyBrush())
    for i in range(16):
      t = theta - i * pi / 16
      color = QColor(255, 144, 0, int(255 - 255 * i / 16))
      painter.setPen(parsePen(color, 2, SolidFill))
      x = origin.x() + r * cos(t)
      y = origin.y() + r * sin(t)
      painter.drawLine(QLineF(origin.toPointF(), QPointF(x, y)))
