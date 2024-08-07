"""Label provides a property driven alternative to QLabel. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Never, Any

from PySide6.QtCore import QSize, QRect, QMargins, Qt, QPoint, QMarginsF, \
  QRectF, QSizeF
from PySide6.QtGui import (QFont, QFontMetrics, QPaintEvent, QPainter,
                           QColor, QPen, QFontMetricsF)
from PySide6.QtWidgets import QWidget, QGridLayout
from icecream import ic
from worktoy.desc import AttriBox, Field, DEFAULT
from worktoy.meta import overload, BaseObject
from worktoy.parse import maybe
from worktoy.text import typeMsg, monoSpace

from ezside.tools import textPen, Align, emptyBrush, fillBrush, parsePen, \
  Font
from ezside.widgets import BoxWidget

ic.configureOutput(includeContext=True)


class Label(BoxWidget):
  """Label provides a property driven alternative to QLabel. """

  __fallback_text__ = 'LABEL'
  __parsed_object__ = None

  font = AttriBox[Font]()
  text = AttriBox[str]()

  rectSize = Field()

  @rectSize.GET
  def _getRectSize(self) -> QSizeF:
    """This method calculates the size required to bound the text."""
    return QFontMetricsF.boundingRect(self.font.metrics, self.text).size()

  @text.ONSET
  def hookedTextSet(self, oldText: str, newText: str) -> None:
    """This method is called when the text is set."""
    if oldText != newText:
      self.adjustSize()
      self.update()

  def paintEvent(self, event: QPaintEvent) -> None:
    """Reimplementation"""
    BoxWidget.paintEvent(self, event)
    painter = QPainter()
    painter.begin(self)
    viewRect = painter.viewport()
    marginRect = QRectF.marginsRemoved(viewRect.toRectF(), self.margins)
    borderRect = QRectF.marginsRemoved(marginRect, self.borders)
    paddedRect = QRectF.marginsRemoved(borderRect, self.paddings)
    self.font @ painter
    painter.drawText(paddedRect, self.font.align.qt, self.text)
    painter.end()

  def __init__(self, *args, ) -> None:
    BoxWidget.__init__(self, *args)
    for arg in args:
      if isinstance(arg, str):
        self.text = arg
        break
    else:
      self.text = self.__fallback_text__
    self.paddings = 1, 4
    self.borders = 2

  def requiredSize(self) -> QSizeF:
    """This method returns the size hint of the widget."""
    return self.rectSize
