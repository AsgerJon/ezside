"""BoxWidget provides a base class for other widgets that need to paint on
a background that supports the box model."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TypeAlias, Union, Never

from PySide6.QtCore import QMargins, QRect, QRectF, QPointF, QSizeF
from PySide6.QtCore import QMarginsF
from PySide6.QtGui import QPaintEvent, QPainter, QColor, QBrush
from PySide6.QtWidgets import QWidget
from icecream import ic
from worktoy.desc import AttriBox, Field
from worktoy.parse import maybe
from worktoy.text import monoSpace, typeMsg

from ezside.tools import fillBrush, emptyPen, SizeRule

Rect: TypeAlias = Union[QRect, QRectF]

ic.configureOutput(includeContext=True)


class BoxWidget(QWidget):
  """BoxWidget provides a base class for other widgets that need to paint on
  a background that supports the box model."""

  __latest_viewport__ = None
  __fallback_size_rule__ = SizeRule.PREFER
  __size_rule__ = None

  aspectRatio = AttriBox[float](-1)  # negative means ignore

  margins = AttriBox[QMarginsF](QMarginsF(0, 0, 0, 0, ))
  borders = AttriBox[QMarginsF](QMarginsF(0, 0, 0, 0, ))
  paddings = AttriBox[QMarginsF](QMarginsF(0, 0, 0, 0, ))
  allMargins = Field()

  sizeRule = Field()

  marginColor = AttriBox[QColor](QColor(0, 0, 0, 0))
  borderColor = AttriBox[QColor](QColor(0, 0, 0, 0))
  backgroundColor = AttriBox[QColor](QColor(0, 0, 0, 0))

  viewRect = Field()
  marginedRect = Field()
  borderedRect = Field()
  paddingRect = Field()
  contentRect = Field()

  marginBrush = Field()
  borderBrush = Field()
  backgroundBrush = Field()

  @sizeRule.GET
  def _getSizeRule(self) -> SizeRule:
    """This method returns the size rule for the widget. """
    return maybe(self.__size_rule__, self.__fallback_size_rule__)

  @sizeRule.SET
  def _setSizeRule(self, rule: SizeRule) -> None:
    """This method sets the size rule for the widget. """
    if not isinstance(rule, SizeRule):
      e = typeMsg('rule', rule, SizeRule)
      raise TypeError(e)
    self.__size_rule__ = rule
    self.setSizePolicy(rule.qt)
    self.adjustSize()
    self.update()

  @allMargins.GET
  def _getAllMargins(self) -> QMargins:
    """This method returns the sum of all margins. """
    return self.margins + self.borders + self.paddings

  @allMargins.SET
  def _setAllMargins(self, value: object) -> Never:
    """Disabled setter for allMargins."""
    e = """The 'allMargins' attribute is read-only, but was attempted to 
    be overwritten to: '%s'!"""
    raise TypeError(monoSpace(e % str(value)))

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
  def _getMarginedRect(self) -> QRectF:
    """This method returns the rectangle of the widget with margins. """
    rect0 = self.__latest_viewport__
    if self.__latest_viewport__ is None:
      rect0 = QRectF(QPointF(0, 0), QWidget.sizeHint(self).toSizeF())
    rect = self._enforceAspect(rect0)
    if isinstance(rect0, QRect):
      newCenter = rect0.center().toPointF()
    else:
      newCenter = rect0.center()
    QRectF.moveCenter(rect, newCenter)
    return rect

  @borderedRect.GET
  def _getBorderedRect(self) -> QRectF:
    """This method returns the rectangle of the widget with borders. """
    rect = QRectF.marginsRemoved(self.marginedRect, self.margins)
    rect = self._enforceAspect(rect)
    QRectF.moveCenter(rect, self.viewRect.center())
    return rect

  @paddingRect.GET
  def _getPaddingRect(self) -> QRectF:
    """This method returns the rectangle of the widget with padding. """
    borderRect = self.borderedRect
    borderMargin = self.borders
    padding0 = QRectF.marginsRemoved(borderRect, borderMargin)
    padding = self._enforceAspect(padding0)
    newCenter = self.viewRect.center()
    QRectF.moveCenter(padding, newCenter)
    return padding

  @contentRect.GET
  def _getContentRect(self) -> QRectF:
    """This method returns the rectangle of the widget with padding. """
    rect = QRectF.marginsRemoved(self.paddingRect, self.paddings)
    rect = self._enforceAspect(rect)
    QRectF.moveCenter(rect, self.viewRect.center())
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
