"""CanvasWidget provides a canvas widget. It supports the box model with
an outer margin, a border and padding. Subclasses should allow the parent
class to paint the background and border before painting the custom
content. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import Any

from PySide6.QtCore import QMargins, \
  QPoint, \
  QRect, \
  QPointF, \
  QRectF, \
  QSizeF, \
  QSize
from PySide6.QtGui import QPaintEvent, QPainter, QColor
from icecream import ic
from vistutils.text import monoSpace

from ezside.widgets import BaseWidget
from ezside.core import parseBrush, SolidFill, emptyPen, AlignTop
from ezside.core import AlignCenter, AlignBottom, AlignVCenter, AlignLeft
from ezside.core import AlignHCenter, AlignRight

ic.configureOutput(includeContext=True)


class _Painter(QPainter):
  """Class implementing restriction on the viewport"""

  __inner_rect__ = None

  def begin(self, *args) -> None:
    """Begins the painting"""
    QPainter.begin(self, *args)
    QPainter.setRenderHint(self, QPainter.RenderHint.Antialiasing)

  def viewport(self) -> QRect:
    """Returns the viewport"""
    if self.__inner_rect__ is None:
      return QPainter.viewport(self)
    return self.__inner_rect__

  def setInnerViewport(self, rect: QRect) -> None:
    """Sets the viewport"""
    # QPainter.setViewport(self, rect)
    self.translate(rect.topLeft())
    self.__inner_rect__ = QRect(QPoint(0, 0), rect.size())

  def end(self) -> None:
    """Ends the painting"""
    self.__inner_rect__ = None
    QPainter.end(self)


class CanvasWidget(BaseWidget):

  @classmethod
  def registerFields(cls) -> dict[str, Any]:
    """The registerFields method registers the fields of the widget.
    Please note, that subclasses can reimplement this method, but must
    provide these same fields. """
    return {
      'margins'        : QMargins(2, 2, 2, 2, ),
      'borders'        : QMargins(2, 2, 2, 2, ),
      'paddings'       : QMargins(2, 2, 2, 2, ),
      'borderColor'    : QColor(0, 0, 0, 255),
      'backgroundColor': QColor(255, 255, 0, 255),
      'radius'         : QPoint(8, 8, ),
      'vAlign'         : AlignVCenter,
      'hAlign'         : AlignHCenter,
    }

  @classmethod
  @abstractmethod
  def registerStates(cls) -> list[str]:
    """The registerStates method registers the states of the widget."""

  @classmethod
  @abstractmethod
  def registerDynamicFields(cls) -> dict[str, Any]:
    """The registerDynamicFields method registers the dynamic fields of the
    widget."""

  @abstractmethod
  def initSignalSlot(self) -> None:
    """The initSignalSlot method connects signals and slots."""

  @abstractmethod
  def initUi(self) -> None:
    """The initUi method initializes the user interface."""

  def alignRect(self, *args) -> QRect:
    """Calculates the aligned rectangle for text"""
    static, moving = None, None
    for arg in args:
      if isinstance(arg, QRectF):
        if static is None:
          static = arg.toRect()
        elif moving is None:
          moving = arg.toRect()
      if isinstance(arg, QRect):
        if static is None:
          static = arg
        elif moving is None:
          moving = arg
      if isinstance(arg, (QSize, QSizeF)):
        if static is None:
          e = """Received a size argument before a rectangle argument!"""
          raise ValueError(monoSpace(e))
        if isinstance(arg, QSizeF):
          moving = arg.toSize()
        else:
          moving = arg
    if static is None or moving is None:
      e = """Missing a rectangle argument!"""
      raise ValueError(monoSpace(e))
    vAlign = self.getStyle('vAlign')
    hAlign = self.getStyle('hAlign')
    staticHeight, movingHeight = static.height(), moving.height()
    staticWidth, movingWidth = static.width(), moving.width()
    if vAlign == AlignTop:
      top = static.top()
    elif vAlign in [AlignCenter, AlignVCenter]:
      top = static.top() + (staticHeight - movingHeight) / 2
    elif vAlign == AlignBottom:
      top = static.bottom() - movingHeight
    else:
      e = """Unrecognized value for vertical alignment: '%s'"""
      raise ValueError(monoSpace(e % str(vAlign)))
    if hAlign == AlignLeft:
      left = static.left()
    elif hAlign in [AlignCenter, AlignHCenter]:
      left = static.left() + (staticWidth - movingWidth) / 2
    elif hAlign == AlignRight:
      left = static.right() - movingWidth
    else:
      e = """Unrecognized value for horizontal alignment: '%s'"""
      raise ValueError(monoSpace(e % str(hAlign)))
    topLeft = QPointF(left, top).toPoint()
    return QRect(topLeft, moving)

  def paintEvent(self, event: QPaintEvent) -> None:
    """The paintEvent method paints the widget."""
    painter = _Painter()
    painter.begin(self)
    viewRect = painter.viewport()
    pen = emptyPen()
    painter.setPen(pen)
    margins = self.getStyle('margins')
    borders = self.getStyle('borders')
    paddings = self.getStyle('paddings')
    backgroundColor = self.getStyle('backgroundColor')
    borderColor = self.getStyle('borderColor')
    backgroundBrush = parseBrush(backgroundColor, SolidFill)
    borderBrush = parseBrush(borderColor, SolidFill)
    radius = self.getStyle('radius')
    if radius is None:
      rx, ry = 0, 0
    else:
      rx, ry = radius.x(), radius.y()
    borderedRect = viewRect - margins
    paddedRect = borderedRect - borders
    innerRect = paddedRect - paddings
    borderedRect.moveCenter(viewRect.center())
    paddedRect.moveCenter(viewRect.center())
    innerRect.moveCenter(viewRect.center())
    painter.setBrush(borderBrush)
    painter.drawRoundedRect(borderedRect, rx, ry)
    painter.setBrush(backgroundBrush)
    painter.drawRoundedRect(paddedRect, rx, ry)
    painter.setInnerViewport(innerRect)
    self.customPaint(painter)
    painter.end()

  def customPaint(self, painter: QPainter) -> None:
    """Subclasses must reimplement this method to define the painting
    action. The painter is already set up and will be ended by the parent
    class. """
