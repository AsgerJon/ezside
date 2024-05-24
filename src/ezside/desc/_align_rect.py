"""The 'alignRect' function receives a source and target rectangle and
aligns the target rectangle to the source rectangle."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QRect, QSize, QSizeF
from PySide6.QtCore import QPointF, QRectF
from icecream import ic
from vistutils.waitaminute import typeMsg

from ezside.desc import AlignLeft, AlignTop, AlignVCenter, AlignCenter
from ezside.desc import AlignRight, AlignHCenter, AlignBottom

ic.configureOutput(includeContext=True)

Rect = QRect | QRectF | QSizeF | QSize
Rects = tuple[Rect, Rect]


def alignRect(self, staticRect: Rect, movingRect: Rect, ) -> QRectF:
  """Calculates the aligned rectangle for text"""
  if isinstance(movingRect, QSizeF):
    newSize = movingRect
  elif isinstance(movingRect, QSize):
    newSize = movingRect.toSizeF()
  elif isinstance(movingRect, QRect):
    newSize = movingRect.size().toSizeF()
  elif isinstance(movingRect, QRectF):
    newSize = movingRect.size()
  else:
    e = typeMsg('movingRect', movingRect, QRect)
    raise TypeError(e)
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
  return QRectF(newTopLeft, newSize)
