"""AbstractSeparator provides a base class for separators."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import Any

from PySide6.QtCore import QLineF, QPointF
from PySide6.QtGui import QColor, QPaintEvent, QPainter

from ezside.widgets import GraffitiVandal
from ezside.widgets.spacers import AbstractSpacer
from ezside.core import Fixed, Expand, emptyPen
from ezside.core import parseBrush, SolidFill, SolidLine, parsePen


class AbstractSeparator(AbstractSpacer):
  """AbstractSeparator provides a base class for separators. """

  @abstractmethod
  def _getHorizontalFlag(self) -> bool:
    """Returns the horizontal flag. True indicates that the separator should
    occupy horizontal space."""

  @abstractmethod
  def _getVerticalFlag(self) -> bool:
    """Returns the vertical flag. True indicates that the separator should
    occupy vertical space."""

  def initUi(self, ) -> None:
    """Initializes the UI."""
    hPol = Expand if self._getHorizontalFlag() else Fixed
    vPol = Expand if self._getVerticalFlag() else Fixed
    self.setSizePolicy(hPol, vPol)

  def customPaint(self, painter: GraffitiVandal) -> None:
    """The customPaint method provides the custom painting for the
    separator."""
    viewRect = painter.viewport()
    left, top, = viewRect.left(), viewRect.top()
    right, bottom = viewRect.right(), viewRect.bottom()
    x0, y0 = viewRect.center().x(), viewRect.center().y()
    if self._getHorizontalFlag():
      line = QLineF(QPointF(left, y0), QPointF(right, y0))
    elif self._getVerticalFlag():
      line = QLineF(QPointF(x0, top), QPointF(x0, bottom))
    else:
      line = QLineF(QPointF(left, top), QPointF(right, bottom))
    painter.setBrush(parseBrush(QColor(0, 0, 0, 31), SolidFill))
    painter.setPen(emptyPen())
    painter.drawRect(viewRect)
    painter.setPen(self.getStyle('separatorPen'))
    painter.drawLine(line)
