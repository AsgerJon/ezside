"""BoxWidget provides a base class for other widgets that need to paint on
a background that supports the box model."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TypeAlias, Union, Optional

from PySide6.QtCore import QRect, QRectF, QSizeF, QSize, QPointF, Qt
from PySide6.QtGui import QPaintEvent, QPainter, QColor, QBrush
from PySide6.QtWidgets import QWidget
from icecream import ic
from worktoy.desc import AttriBox, Field
from worktoy.meta import BaseObject, overload
from worktoy.parse import maybe
from worktoy.text import monoSpace, typeMsg

from ezside.tools import fillBrush, emptyPen, SizeRule, MarginsBox, ColorBox

Rect: TypeAlias = Union[QRect, QRectF]

ic.configureOutput(includeContext=True)


class BoxWidget(QWidget):
  """BoxWidget provides a base class for other widgets that need to paint on
  a background that supports the box model."""

  __suppress_notifiers__ = None

  margins = MarginsBox(0)
  paddings = MarginsBox(0)
  borders = MarginsBox(0)
  sizeRule = AttriBox[SizeRule](SizeRule.PREFER)
  borderColor = ColorBox(QColor(0, 0, 0, 255))
  backgroundColor = ColorBox(QColor(255, 255, 255, 255))
  borderBrush = Field()
  backgroundBrush = Field()
  aspectRatio = AttriBox[float](-1)  # -1 means ignore

  @borderBrush.GET
  def _getBorderBrush(self) -> QBrush:
    """Getter-function for the borderBrush."""
    return fillBrush(self.borderColor, )

  @backgroundBrush.GET
  def _getBackgroundBrush(self) -> QBrush:
    """Getter-function for the backgroundBrush."""
    return fillBrush(self.backgroundColor, )

  def paintEvent(self, event: QPaintEvent) -> None:
    """Paints the widget."""
    painter = QPainter()
    painter.begin(self)
    viewRect = painter.viewport()
    center = viewRect.center()
    marginRect = QRectF.marginsRemoved(viewRect.toRectF(), self.margins)
    borderRect = QRectF.marginsRemoved(marginRect, self.borders)
    paddedRect = QRectF.marginsRemoved(borderRect, self.paddings)
    marginRect.moveCenter(center)
    borderRect.moveCenter(center)
    paddedRect.moveCenter(center)
    painter.setPen(emptyPen())
    painter.setBrush(self.borderBrush)
    painter.drawRect(marginRect)
    painter.setBrush(self.backgroundBrush)
    painter.drawRect(borderRect)
    painter.end()

  def resize(self, *args) -> None:
    """Reimplementation enforcing aspect ratio. """
    if self.aspectRatio >= 0 and not self.sizeRule.base:
      e = """Incompatible settings! Aspect ratio enforcement require 
      isotropic size policy!"""
      raise ValueError(monoSpace(e))
    if self.aspectRatio < 0:
      return QWidget.resize(self, *args)
    size = (*args, None)[0]
    if not isinstance(size, (QSize, QSizeF)):
      return QWidget.resize(self, *args)
    height, width = size.height(), size.width()
    if width / height > self.aspectRatio:
      newSize = QSize(height * self.aspectRatio, height)
    else:
      newSize = QSize(width, width / self.aspectRatio)
    QWidget.resize(self, newSize)

  @margins.ONSET
  @borders.ONSET
  @paddings.ONSET
  def _updateBoxModel(self,
                      oldVal: MarginsBox,
                      newVal: MarginsBox) -> None:
    """Setter-hook for changes to the box model."""
    if oldVal != newVal:
      self.adjustSize()
      self.update()

  @sizeRule.ONSET
  def _updateSizeRule(self, oldRule: SizeRule, newRule: SizeRule) -> None:
    """Setter-hook for changes to the size rule. """
    if oldRule != newRule:
      QWidget.setSizePolicy(self, newRule.qt)
      self.adjustSize()
      self.update()

  def requiredSize(self) -> QSizeF:
    """Subclasses may implement this method to define minimum size
    requirements. """
    return QSizeF(0, 0)

  def minimumSizeHint(self) -> QSize:
    """This method returns the size hint of the widget."""
    rect = QRectF(QPointF(0, 0), self.requiredSize())
    rect += self.margins
    rect += self.borders
    rect += self.paddings
    return QRectF.toRect(rect, ).size()

  def __init__(self, *args) -> None:
    for arg in args:
      if isinstance(arg, QWidget):
        QWidget.__init__(self, arg)
        break
    else:
      QWidget.__init__(self)
    sizeRule = None
    for arg in args:
      if isinstance(arg, SizeRule):
        if sizeRule is None:
          sizeRule = arg
        else:
          sizeRule += arg
    self.sizeRule = maybe(sizeRule, SizeRule.PREFER)
