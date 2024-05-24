"""CanvasWidget is a subclass of CoreWidget implementing box-model painting:
  - Full viewport
  - Including borders, excluding margins
  - Including padding, excluding borders
  - Including inner contents, excluding padding

Subclasses should implement the 'customPaint' method, which receives a
painter that defines its viewport as the inner content area. The subclass
can then use this painter to draw its contents.

The painter is an instance of GraffitiVandal which is a subclass of
QPainter. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QPaintEvent

from ezside.desc import emptyPen, emptyBrush, SolidFill, parseBrush
from ezside.desc import Black, White, Point, Margins
from ezside.widgets import CoreWidget, GraffitiVandal


class CanvasWidget(CoreWidget):
  """CanvasWidget is a subclass of CoreWidget implementing box-model
  painting:
    - Full viewport
    - Including borders, excluding margins
    - Including padding, excluding borders
    - Including inner contents, excluding padding

  Subclasses should implement the 'customPaint' method, which receives a
  painter that defines its viewport as the inner content area. The subclass
  can then use this painter to draw its contents.

  The painter is an instance of GraffitiVandal which is a subclass of
  QPainter. """

  cornerRadius = Point(2, 2)
  marginGeometry = Margins(2, 2, 2, 2)
  borderGeometry = Margins(2, 2, 2, 2, )
  paddingGeometry = Margins(8, 8, 8, 8, )
  marginBrush = emptyBrush()
  borderBrush = parseBrush(Black, SolidFill)
  paddingBrush = parseBrush(White, SolidFill)

  def paintEvent(self, event: QPaintEvent) -> None:
    """The paintEvent method paints the widget."""
    painter = GraffitiVandal()
    painter.begin(self)
    viewRect = painter.viewport()
    painter.setPen(emptyPen())
    rx, ry = self.cornerRadius.x(), self.cornerRadius.y()
    borderedRect = viewRect - self.marginGeometry
    paddedRect = borderedRect - self.borderGeometry
    innerRect = paddedRect - self.paddingGeometry
    borderedRect.moveCenter(viewRect.center())
    paddedRect.moveCenter(viewRect.center())
    innerRect.moveCenter(viewRect.center())
    painter.setBrush(self.marginBrush)
    painter.drawRoundedRect(viewRect, rx, ry)
    painter.setBrush(self.borderBrush)
    painter.drawRoundedRect(borderedRect, rx, ry)
    painter.setBrush(self.paddingBrush)
    painter.drawRoundedRect(paddedRect, rx, ry)
    painter.setInnerViewport(innerRect)
    self.customPaint(painter)
    painter.end()

  def customPaint(self, painter: GraffitiVandal) -> None:
    """The customPaint method should be implemented by subclasses to
    paint the inner contents of the widget."""
