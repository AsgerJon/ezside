"""BoxWidget provides a base class for other widgets that need to paint on
a background that supports the box model."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QMargins
from PySide6.QtGui import QPaintEvent, QPainter, QColor, QBrush
from PySide6.QtWidgets import QWidget
from worktoy.desc import AttriBox

from ezside.tools import fillBrush, emptyPen


class BoxWidget(QWidget):
  """BoxWidget provides a base class for other widgets that need to paint on
  a background that supports the box model."""

  backgroundColor = AttriBox[QColor](QColor(169, 255, 0, 255))
  textColor = AttriBox[QColor](QColor(0, 0, 0, 255))
  borderColor = AttriBox[QColor](QColor(0, 0, 0, 255))

  def _getMargin(self) -> QMargins:
    """Getter-function for the margins."""
    return QMargins(2, 2, 2, 2, )

  def _getBorder(self) -> QMargins:
    """Getter-function for the border."""
    return QMargins(1, 1, 1, 1, )

  def _getPadding(self) -> QMargins:
    """Getter-function for the padding."""
    return QMargins(2, 2, 2, 2, )

  def _getBorderBrush(self) -> QBrush:
    """Getter-function for the border brush."""
    return fillBrush(self.borderColor)

  def _getPaddingBrush(self, ) -> QBrush:
    """Getter-function for the padding brush."""
    return fillBrush(self.backgroundColor)

  def _getBackgroundBrush(self) -> QBrush:
    """Getter-function for the background brush."""
    return fillBrush(self.backgroundColor)

  def paintEvent(self, event: QPaintEvent) -> None:
    """This method handles painting of the widget"""
    painter = QPainter()
    painter.begin(self)
    viewRect = painter.viewport()
    marginedRect = viewRect.marginsRemoved(self._getMargin())
    borderedRect = marginedRect.marginsRemoved(self._getBorder())
    paddedRect = borderedRect.marginsRemoved(self._getPadding())
    painter.setPen(emptyPen())
    painter.setBrush(self._getBorderBrush())
    painter.drawRect(borderedRect)
    painter.setBrush(self._getPaddingBrush())
    painter.drawRect(paddedRect)
    painter.setBrush(self._getBackgroundBrush())
    painter.drawRect(marginedRect)
    painter.end()
