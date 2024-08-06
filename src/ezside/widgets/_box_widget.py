"""BoxWidget provides a base class for other widgets that need to paint on
a background that supports the box model."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TypeAlias, Union, Never, Optional

from PySide6.QtCore import QMargins, QRect, QRectF, QPointF, QSizeF, QSize
from PySide6.QtCore import QMarginsF
from PySide6.QtGui import QPaintEvent, QPainter, QColor, QBrush
from PySide6.QtWidgets import QWidget
from icecream import ic
from worktoy.desc import AttriBox, Field
from worktoy.ezdata import EZData
from worktoy.meta import BaseObject, overload
from worktoy.parse import maybe
from worktoy.text import monoSpace, typeMsg

from ezside.tools import fillBrush, emptyPen, SizeRule, MarginsBox, Align, \
  ColorBox

Rect: TypeAlias = Union[QRect, QRectF]

ic.configureOutput(includeContext=True)


class _Parse(BaseObject):
  """External overloading class"""

  __parent_widget__ = None
  __size_rule__ = None
  __fallback_size_rule__ = SizeRule.PREFER

  parent = Field()
  sizeRule = Field()

  @parent.GET
  def _getParent(self) -> Optional[QWidget]:
    """Getter-function for the parent."""
    return maybe(self.__parent_widget__, None)

  @sizeRule.GET
  def _getSizeRule(self) -> SizeRule:
    """Getter-function for the 'sizeRule'."""
    return maybe(self.__size_rule__, self.__fallback_size_rule__)

  @overload(SizeRule, QWidget)
  def __init__(self, sizePolicy: SizeRule, parent: QWidget) -> None:
    """Overloaded constructor"""
    self.__parent_widget__ = parent
    self.__size_policy__ = sizePolicy

  @overload(QWidget, SizeRule)
  def __init__(self, parent: QWidget, sizePolicy: SizeRule) -> None:
    """Overloaded constructor"""
    self.__parent_widget__ = parent
    self.__size_policy__ = sizePolicy

  @overload(QWidget)
  def __init__(self, parent: QWidget) -> None:
    """Overloaded constructor"""
    self.__parent_widget__ = parent

  @overload()
  def __init__(self) -> None:
    """Overloaded constructor"""
    pass


class BoxWidget(QWidget):
  """BoxWidget provides a base class for other widgets that need to paint on
  a background that supports the box model."""

  margins = MarginsBox(1)
  paddings = MarginsBox(1)
  borders = MarginsBox(1)
  sizeRule = AttriBox[SizeRule](SizeRule.PREFER)
  borderColor = ColorBox(QColor(0, 0, 0, 255))
  borderBrush = Field()
  backgroundColor = ColorBox(QColor(255, 255, 255, 255))
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
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    viewRect = painter.viewport()
    borderRect = QRectF.marginsRemoved(viewRect.toRectF(), self.borders)
    paddedRect = QRectF.marginsRemoved(borderRect, self.paddings)
    painter.setPen(emptyPen())
    painter.setBrush(self.borderBrush)
    painter.drawRect(borderRect)
    painter.setBrush(self.backgroundBrush)
    painter.drawRect(paddedRect)
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

  @sizeRule.ONSET
  def _updateSizeRule(self, oldRule: SizeRule, newRule: SizeRule) -> None:
    """Setter-hook for changes to the size rule. """
    if oldRule == newRule:
      return  # ignore

  def __init__(self, *args) -> None:
    self.parsed = (*args,)
    if not isinstance(self.parsed, _Parse):
      e = typeMsg('parsed', self.parsed, _Parse)
      raise TypeError(e)
    QWidget.__init__(self, self.parsed.parent)
    Field.silenceInstance(type(self).sizeRule, self)
    self.sizeRule = self.parsed.sizeRule
    QWidget.setSizePolicy(self, self.sizeRule.qt)
    Field.unsilenceInstance(type(self).sizeRule, self)
