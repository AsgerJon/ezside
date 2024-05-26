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

from typing import TYPE_CHECKING

from PySide6.QtCore import QMargins, QPoint
from PySide6.QtGui import QPaintEvent, QBrush
from vistutils.fields import EmptyField

from ezside.desc import emptyPen, emptyBrush, SolidFill, parseBrush
from ezside.desc import Black, White
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

  __fallback_corner_radius__ = QPoint(2, 2)
  __fallback_margin_geometry__ = QMargins(2, 2, 2, 2)
  __fallback_border_geometry__ = QMargins(2, 2, 2, 2)
  __fallback_padding_geometry__ = QMargins(8, 8, 8, 8)
  __fallback_margin_brush__ = emptyBrush()
  __fallback_border_brush__ = parseBrush(Black, SolidFill)
  __fallback_padding_brush__ = parseBrush(White, SolidFill)

  cornerRadius = EmptyField()
  marginGeometry = EmptyField()
  borderGeometry = EmptyField()
  paddingGeometry = EmptyField()
  marginBrush = EmptyField()
  borderBrush = EmptyField()
  paddingBrush = EmptyField()

  @cornerRadius.GET
  def _getCornerRadius(self) -> QPoint:
    """Getter-function for corner radius"""
    return self.__fallback_corner_radius__

  @marginGeometry.GET
  def _getMargins(self) -> QMargins:
    """Getter-function for margins"""
    return self.__fallback_margin_geometry__

  @borderGeometry.GET
  def _getBorders(self) -> QMargins:
    """Getter-function for borders"""
    return self.__fallback_border_geometry__

  @paddingGeometry.GET
  def _getPaddings(self) -> QMargins:
    """Getter-function for paddings"""
    return self.__fallback_padding_geometry__

  @marginBrush.GET
  def _getMarginBrush(self, ) -> QBrush:
    """Getter-function for margin brush"""
    return emptyBrush()

  @borderBrush.GET
  def _getBorderBrush(self, ) -> QBrush:
    """Getter-function for border brush"""
    return parseBrush(Black, SolidFill)

  @paddingBrush.GET
  def _getPaddingBrush(self, ) -> QBrush:
    """Getter-function for padding brush"""
    return parseBrush(White, SolidFill)

  def paintEvent(self, event: QPaintEvent) -> None:
    """The paintEvent method paints the widget."""
    if TYPE_CHECKING:
      assert isinstance(self.marginBrush, QBrush)
      assert isinstance(self.borderBrush, QBrush)
      assert isinstance(self.paddingBrush, QBrush)
      assert isinstance(self.marginGeometry, QMargins)
      assert isinstance(self.borderGeometry, QMargins)
      assert isinstance(self.paddingGeometry, QMargins)
      assert isinstance(self.cornerRadius, QPoint)
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
