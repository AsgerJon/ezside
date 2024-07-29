"""BoxWidget provides a base class for other widgets that need to paint on
a background that supports the box model."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TypeAlias, Union

from PySide6.QtCore import QMargins, QRect, QRectF, QPointF, QSizeF
from PySide6.QtGui import QPaintEvent, QPainter, QColor, QBrush
from PySide6.QtWidgets import QWidget
from worktoy.desc import AttriBox, EmptyField
from worktoy.parse import maybe

from ezside.tools import fillBrush, emptyPen

Rect: TypeAlias = Union[QRect, QRectF]


class BoxWidget(QWidget):
  """BoxWidget provides a base class for other widgets that need to paint on
  a background that supports the box model."""

  __latest_viewport__ = None

  aspectRatio = AttriBox[float](-1)  # negative means ignore

  margins = AttriBox[QMargins](QMargins(0, 0, 0, 0, ))
  border = AttriBox[QMargins](QMargins(0, 0, 0, 0, ))
  padding = AttriBox[QMargins](QMargins(0, 0, 0, 0, ))

  marginColor = AttriBox[QColor](QColor(0, 0, 0, 0))
  borderColor = AttriBox[QColor](QColor(0, 0, 0, 0))
  backgroundColor = AttriBox[QColor](QColor(0, 0, 0, 0))

  viewRect = EmptyField()
  marginedRect = EmptyField()
  borderedRect = EmptyField()
  paddingRect = EmptyField()
  contentRect = EmptyField()

  marginBrush = EmptyField()
  borderBrush = EmptyField()
  backgroundBrush = EmptyField()

  @marginBrush.GET
  def _getMarginBrush(self) -> QBrush:
    """This method returns the brush used to paint the margins. """
    return fillBrush(self.marginColor)

  @borderBrush.GET
  def _getBorderBrush(self) -> QBrush:
    """This method returns the brush used to paint the borders. """
    return fillBrush(self.borderColor)

  @backgroundBrush.GET
  def _getBackgroundBrush(self) -> QBrush:
    """This method returns the brush used to paint the background. """
    return fillBrush(self.backgroundColor)

  @viewRect.GET
  @marginedRect.GET
  def _getMarginedRect(self) -> QRect:
    """This method returns the rectangle of the widget with margins. """
    rect0 = maybe(self.__latest_viewport__, self.geometry())
    rect = self._enforceAspect(rect0).toRect()
    QRect.moveCenter(rect, rect0.center())
    return rect

  @borderedRect.GET
  def _getBorderedRect(self) -> QRect:
    """This method returns the rectangle of the widget with borders. """
    rect = QRect.marginsRemoved(self.marginedRect, self.margins)
    rect = self._enforceAspect(rect).toRect()
    QRect.moveCenter(rect, self.viewRect.center())
    return rect

  @paddingRect.GET
  def _getPaddingRect(self) -> QRect:
    """This method returns the rectangle of the widget with padding. """
    rect = QRect.marginsRemoved(self.borderedRect, self.border)
    rect = self._enforceAspect(rect).toRect()
    QRect.moveCenter(rect, self.viewRect.center())
    return rect

  @contentRect.GET
  def _getContentRect(self) -> QRect:
    """This method returns the rectangle of the widget with padding. """
    rect = QRect.marginsRemoved(self.paddingRect, self.padding)
    rect = self._enforceAspect(rect).toRect()
    QRect.moveCenter(rect, self.viewRect.center())
    return rect

  def _enforceAspect(self, rect: Rect) -> QRectF:
    """This method returns the largest rectangle that would fit in the
    given rect subject to the aspect ratio."""
    if self.aspectRatio < 0:
      if isinstance(rect, QRectF):
        return rect
      return QRect.toRectF(rect)
    width, height = rect.width(), rect.height()
    if height > width * self.aspectRatio:
      height = width * self.aspectRatio
    if width > height / self.aspectRatio:
      width = height / self.aspectRatio
    return QRectF(QPointF(0, 0), QSizeF(width, height))

  def paintEvent(self, event: QPaintEvent) -> None:
    """This method is triggered when the widget needs to be repainted. """
    painter = QPainter()
    painter.begin(self)
    #  Record the viewport
    self.__latest_viewport__ = painter.viewport()
    #  This box model does not use QPen so set to emptyPen
    painter.setPen(emptyPen())
    #  Draw the rectangle including margin
    painter.setBrush(self.marginBrush)
    painter.drawRect(self.marginedRect)
    #  Draw the rectangle including border, but not margin
    painter.setBrush(self.borderBrush)
    painter.drawRect(self.borderedRect)
    #  Draw the rectangle including padding, but not border
    painter.setBrush(self.backgroundBrush)
    painter.drawRect(self.paddingRect)
    painter.end()
