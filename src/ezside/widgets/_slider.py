"""Slider provides a custom-made alternative to the ugly QSlider."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QSize, QPoint, QRect, QEvent, QPointF
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QWidget

from ezside.widgets import BaseWidget


class Slider(BaseWidget):
  """Slider provides a custom-made alternative to the ugly QSlider."""

  __inner_value__ = 0.5
  __old_value__ = 0.5
  __grab_value__ = 0.5
  __handle_grab__ = False

  def getHandleRect(self, ) -> QRect:
    """Return the rectangle of the handle."""
    width = self.width() - 2
    height = 16
    origin = QPoint(0, 0)
    size = QSize(width, height)
    rect = QRect(origin, size)
    xCenter = self.width() / 2
    outerHeight = self.height()
    innerHeight = outerHeight - height
    yCenter = (1 - self.__inner_value__) * innerHeight + height / 2
    newCenter = QPointF(xCenter, yCenter).toPoint()
    rect.moveCenter(newCenter)
    return rect

  def mousePressEvent(self, event: QMouseEvent) -> None:
    """Set the value of the slider based on the mouse position."""
    handleRect = self._getHandleRect()
    top, bottom = handleRect.top(), handleRect.bottom()
    if top <= event.y() <= bottom:
      self._grabHandle()

  def mouseReleaseEvent(self, event: QMouseEvent) -> None:
    """Release the handle."""
    self._releaseHandle()

  def leaveEvent(self, event: QEvent) -> None:
    """Release the handle."""
    self._cancelGrab()
