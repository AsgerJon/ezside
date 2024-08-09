"""BoxWidget provides a base class for other basewidgets that need to
paint on
a background that supports the box model."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TypeAlias, Union, TYPE_CHECKING, Any

from PySide6.QtCore import QRect, QRectF, QSizeF, QSize, QMarginsF
from PySide6.QtGui import QPainter, QColor, QBrush, QPaintEvent
from PySide6.QtWidgets import QWidget
from icecream import ic
from worktoy.desc import AttriBox, Field

from ezside.basewidgets import LayoutWidget
from ezside.tools import fillBrush, emptyPen, MarginsBox, ColorBox

if TYPE_CHECKING:
  pass

Rect: TypeAlias = Union[QRect, QRectF]

ic.configureOutput(includeContext=True)


class BoxWidget(LayoutWidget):
  """BoxWidget provides a base class for other base widgets that need to
  paint on a background that supports the box model."""

  __suppress_notifiers__ = None

  aspectRatio = AttriBox[float](-1)  # -1 means ignore
  margins = MarginsBox(0)
  paddings = MarginsBox(0)
  borders = MarginsBox(0)
  allMargins = Field()

  borderColor = ColorBox(QColor(0, 0, 0, 0))
  backgroundColor = ColorBox(QColor(0, 0, 0, 0))

  borderBrush = Field()
  backgroundBrush = Field()

  @allMargins.GET
  def _getAllMargins(self) -> QMarginsF:
    """Getter-function for the allMargins."""
    return self.margins + self.paddings + self.borders

  @borderBrush.GET
  def _getBorderBrush(self) -> QBrush:
    """Getter-function for the borderBrush."""
    return fillBrush(self.borderColor, )

  @backgroundBrush.GET
  def _getBackgroundBrush(self) -> QBrush:
    """Getter-function for the backgroundBrush."""
    return fillBrush(self.backgroundColor, )

  def resize(self, newSize: QSize) -> None:
    """Reimplementation enforcing aspect ratio. """
    if self.aspectRatio < 0:
      return QWidget.resize(self, newSize)
    height, width = newSize.height(), newSize.width()
    if width / height > self.aspectRatio:
      newSize = QSizeF(height * self.aspectRatio, height)
    else:
      newSize = QSizeF(width, width / self.aspectRatio)
    QWidget.resize(self, QSizeF.toSize(newSize))

  def paintMeLike(self,
                  rect: Rect,
                  painter: QPainter,
                  event: QPaintEvent) -> Any:
    """Subclasses should implement this method to specify how to paint
    them. When used in a layout from 'ezside.layouts', only this method
    can specify painting, as QWidget.paintEvent will not be called.

    The painter and rectangle passed are managed by the layout and
    base widgets
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
    return paddedRect, painter, event
