"""The 'alignRect' function receives a source and target rectangle and
aligns the target rectangle to the source rectangle."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QRect
from PySide6.QtCore import QPointF, QRectF
from icecream import ic

from ezside.core import AlignLeft, AlignTop, AlignVCenter, AlignCenter
from ezside.core import AlignRight, AlignHCenter, AlignBottom

ic.configureOutput(includeContext=True)

Rect = QRect | QRectF
Rects = tuple[Rect, Rect]


def alignRect(self, staticRect: Rect, movingRect: Rect) -> QRectF:
  """Calculates the aligned rectangle for text"""
  newSize = movingRect.size().tosizeF()
  newLeft, newTop = None, None
  if self.hAlign == AlignLeft:
    newLeft = staticRect.left()
  elif self.hAlign in [AlignHCenter, AlignCenter]:
    newCenterX = staticRect.center().x()
    newLeft = newCenterX - newSize.width() / 2
  elif self.hAlign == AlignRight:
    newLeft = staticRect.right() - newSize.width()
  if self.vAlign == AlignTop:
    newTop = staticRect.top()
  elif self.vAlign in [AlignVCenter, AlignCenter]:
    newCenterY = staticRect.center().y()
    newTop = newCenterY - newSize.height() / 2
  elif self.vAlign == AlignBottom:
    newTop = staticRect.bottom() - newSize.height()
  newTopLeft = QPointF(newLeft, newTop)
  return QRectF(newTopLeft, newSize.toSize())
