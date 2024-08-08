"""BoxWidget provides a base class for other widgets that need to paint on
a background that supports the box model."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TypeAlias, Union, Optional

from PySide6.QtCore import QRect, QRectF, QSizeF, QSize, QPointF, Qt, \
  QMarginsF
from PySide6.QtGui import QPaintEvent, QPainter, QColor, QBrush
from PySide6.QtWidgets import QWidget, QLayout, QMainWindow
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
  __parent_widget__ = None
  __main_window__ = None

  margins = MarginsBox(0)
  paddings = MarginsBox(0)
  borders = MarginsBox(0)
  allMargins = Field()
  sizeRule = AttriBox[SizeRule](SizeRule.PREFER)
  aspectRatio = AttriBox[float](-1)  # -1 means ignore
  borderColor = ColorBox(QColor(0, 0, 0, 255))
  backgroundColor = ColorBox(QColor(255, 255, 255, 255))
  borderBrush = Field()
  backgroundBrush = Field()
  parentWidget = Field()
  mainWindow = Field()

  @allMargins.GET
  def _getAllMargins(self) -> QMarginsF:
    """Getter-function for the allMargins."""
    return self.margins + self.paddings + self.borders

  @parentWidget.GET
  def _getParentWidget(self) -> Optional[QWidget]:
    """Getter-function for the parentWidget."""
    return self.__parent_widget__

  @parentWidget.SET
  def _setParentWidget(self, parentWidget: QWidget) -> None:
    """Setter-function for the parentWidget."""
    if not isinstance(parentWidget, QWidget):
      e = typeMsg('parentWidget', parentWidget, QWidget)
      raise TypeError(e)
    self.__parent_widget__ = parentWidget

  @mainWindow.GET
  def _getMainWindow(self) -> Optional[QWidget]:
    """Getter-function for the mainWindow."""
    return self.__main_window__

  @mainWindow.SET
  def _setMainWindow(self, mainWindow: QMainWindow) -> None:
    """Setter-function for the mainWindow."""
    if not isinstance(mainWindow, QMainWindow):
      e = typeMsg('mainWindow', mainWindow, QMainWindow)
      raise TypeError(e)
    self.__main_window__ = mainWindow

  @borderBrush.GET
  def _getBorderBrush(self) -> QBrush:
    """Getter-function for the borderBrush."""
    return fillBrush(self.borderColor, )

  @backgroundBrush.GET
  def _getBackgroundBrush(self) -> QBrush:
    """Getter-function for the backgroundBrush."""
    return fillBrush(self.backgroundColor, )

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

  def requiredRect(self) -> QRectF:
    """This method returns the required rectangle to bound the current
    widget."""
    size = self.requiredSize()
    return QRectF(QPointF(0, 0), size)

  def minimumSizeHint(self) -> QSize:
    """This method returns the size hint of the widget."""
    rect = QRectF(QPointF(0, 0), self.requiredSize()) + self.allMargins
    return QRectF.toRect(rect, ).size()

  def paintMeLike(self, rect: Rect, painter: QPainter) -> None:
    """Subclasses should implement this method to specify how to paint
    them. When used in a layout from 'ezside.layouts', only this method
    can specify painting, as QWidget.paintEvent will not be called.

    The painter and rectangle passed are managed by the layout and widgets
    are expected to draw only inside the given rect. The layout ensures
    that this rect is at least the exact size specified by the
    'requiredSize' method on this widget. """
    viewRect = rect if isinstance(rect, QRectF) else QRect.toRectF(rect)
    center = viewRect.center()
    marginRect = QRectF.marginsRemoved(viewRect, self.margins)
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

  def __init__(self, *args) -> None:
    for arg in args:
      if isinstance(arg, QMainWindow):
        self.mainWindow = arg
      elif isinstance(arg, QWidget):
        self.parentWidget = arg
    QWidget.__init__(self)
